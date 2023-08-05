from PIL import Image
import numpy as np
from numpy.linalg import eigvals

import sys

from multiprocessing.connection import Client

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QScrollArea, \
    QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QTableWidgetItem, \
    QTableWidget, QSizePolicy, QSpacerItem, QGraphicsLineItem, \
    QCheckBox
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

import pyqtgraph as pg

import skimage.io
from skimage.measure import block_reduce, moments, moments_central

import scipy.optimize as opt

from io import BytesIO
from time import sleep
import argparse

def gaussian2D(xy, amplitude, background, x0, y0, sigma_x, sigma_y, theta=0):
    """ 2D Gaussian with arbitrary rotation

    Args:
        xy (tuple of 2D np.array): meshgrid tuple, specifying the x and y coordinates the function is evaluated at
        amplitude (float): amplitude of the 2D gaussian at x=y=0
        background (float): constant offset
        x0 (float): x-coordinate of center point
        y0 (float): y-coordinate of center point
        sigma_x (float): standard dev. of gaussian along x (after possible rotation)
        sigma_y (float): standard dev. of gaussian along y (after possible rotation)
        theta (float): rotation angle in xy-plane (0 by default)

    Returns:
        1D np.array: 1D vector, resulting of concatenated row vectors making up the 2D matrix that shows the 2D gaussian
    """
    x, y = xy
    if sigma_x < 0 or sigma_y < 0:
        return np.inf
    a = (np.cos(theta) ** 2) / (2 * sigma_x ** 2) + (np.sin(theta) ** 2) / (2 * sigma_y ** 2)
    b = -(np.sin(2 * theta)) / (4 * sigma_x ** 2) + (np.sin(2 * theta)) / (4 * sigma_y ** 2)
    c = (np.sin(theta) ** 2) / (2 * sigma_x ** 2) + (np.cos(theta) ** 2) / (2 * sigma_y ** 2)
    g = background + amplitude * np.exp(- (a * ((x - x0) ** 2) + 2 * b * (x - x0) * (y - y0) + c * ((y - y0) ** 2)))
    return g.ravel()

def get_centroid_info(image, noise_threshold=0.4):
    #get cloud center estimate from centroid
    try:
        #get maximum amplitude estimate of data and cut off noise relative to this level
        bs = 4 #block reduce image by 4x4 pixels to prevent dead pixels from contributing to maximum estimate
        reduced_frame = block_reduce(image, block_size=(bs, bs), func=np.mean)
        max_amp = np.max(reduced_frame)
        data = image.copy()
        data[data<(noise_threshold*max_amp)] = 0

        m1 = moments(data, order=1)
        centroid = (m1[1, 0] / m1[0, 0], m1[0, 1] / m1[0, 0])
        print('centroid ', centroid)

        #get rotation angle and main axes
        mc2 = moments_central(data, cr=np.round(centroid[1]), cc=np.round(centroid[0]), order=2)
        #print(mc2)
        cov = np.array([[mc2[2,0], mc2[1,1]],[mc2[1,1],mc2[0,2]]])/mc2[0,0]
        eigs = eigvals(cov)
        #print(eigs)
        if mc2[2,0] == mc2[0,2]:
            angle = 0
        else:
            angle = -0.5*np.arctan(2*mc2[1,1]/(mc2[2,0]-mc2[0,2]))
        #print('centroid angle', angle)

        return {'x0': centroid[0], 'y0':centroid[1], 'main1_var': eigs[0], 'main2_var': eigs[1], 'angle': angle}

    except Exception as e:
        print('centroid extraction failed: ', e)
        return {'x0': 1 , 'y0': 1, 'main1_var': 1, 'main2_var': 1, 'angle': 0}

def fit_gaussian(image, initial_guess=None):
    block_sizes = [4,1]

    if initial_guess is None:
        centroid = get_centroid_info(image)
        guess = np.array([np.max(image),0,\
                centroid['x0'], centroid['y0'],\
                np.sqrt(centroid['main1_var']),np.sqrt(centroid['main2_var']),\
                centroid['angle']])
    else:
        guess = initial_guess

    for bs in block_sizes:
        print(bs)
        reduced_frame = block_reduce(image, block_size=(bs, bs), func=np.mean)
        guess[2:6] = guess[2:6] *  1./bs
        y, x = np.indices(reduced_frame.shape)
        xy = (x,y)
        try:
            popt, pcov = opt.curve_fit(gaussian2D, xy, \
                reduced_frame.ravel(),\
                p0=guess)
            popt[2:6] *= bs
            print(popt)
            guess = popt

        except Exception as e:
            print(e)
            print('Fit not possible.')
            return {'x0': guess[2], 'y0': guess[3], 'main1_sigma': guess[4], 'main2_sigma': guess[5], 'angle': guess[6]}

    return {'x0': popt[2], 'y0': popt[3], 'main1_sigma': popt[4], 'main2_sigma': popt[5], 'angle': popt[6]}

def image_from_stream_object(frame):
    """
    function to turn object that was transferred via the socket connection into a 2D numpy array
    """
    print(sys.getsizeof(frame))
    data = skimage.io.imread(frame, as_grey=True)
    #data = block_reduce(data, block_size=(4, 4), func=np.mean)
    data = ((data - data.min()) / (data.ptp() / 255.0)).astype(np.uint8) # map the data range to 0 - 255
    return data

class CameraViewer(QMainWindow):
    capture_request = pyqtSignal()

    def __init__(self, cam_hostname='campi.local'):
        super(CameraViewer, self).__init__()

        layout_split = QHBoxLayout()
        layout_viewer = QVBoxLayout()
        layout_fits = QVBoxLayout()
        layout_split.addLayout(layout_viewer)
        layout_split.addLayout(layout_fits)

        # VIEWER
        b = QPushButton("Save frame")
        b.pressed.connect(self.save_frame)
        layout_viewer.addWidget(b)

        self.cam_hostname = cam_hostname
        self.setup_and_start_camera_thread()

        self.frame_counter = 0

        self.resolution = self.cam.resolution
        print(self.resolution)
        self.pixel_size = self.cam.pixel_size
        print(self.pixel_size)

        self.imv = pg.ImageView()
        self.imv.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout_viewer.addWidget(self.imv)

        #Fit enable checkbox
        self.enable_fit = False
        self.fit_cb = QCheckBox('enable fit', self)
        self.fit_cb.stateChanged.connect(self.change_fit_cb)
        layout_fits.addWidget(self.fit_cb)

        #CENTROID RESULTS
        layout_fits.addWidget(QLabel('Centroid results'))
        self.centroid_widget = QTableWidget()
        self.centroid_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.centroid_widget.setRowCount(5)
        self.centroid_widget.setColumnCount(2)
        self.centroid_widget.setItem(0,0, QTableWidgetItem("x0"))
        self.centroid_widget.setItem(0,1, QTableWidgetItem("1"))
        self.centroid_widget.setItem(1,0, QTableWidgetItem("y0"))
        self.centroid_widget.setItem(1,1, QTableWidgetItem("1"))
        self.centroid_widget.setItem(2,0, QTableWidgetItem("main1_waist"))
        self.centroid_widget.setItem(2,1, QTableWidgetItem("1"))
        self.centroid_widget.setItem(3,0, QTableWidgetItem("main2_waist"))
        self.centroid_widget.setItem(3,1, QTableWidgetItem("1"))
        self.centroid_widget.setItem(4,0, QTableWidgetItem("angle"))
        self.centroid_widget.setItem(4,1, QTableWidgetItem("1"))
        self.centroid_widget.move(0,0)
        layout_fits.addWidget(self.centroid_widget)

        #self.centroid_crosshair = QGraphicsLineItem(200,200,300,300)
        #self.imv.addItem(self.centroid_crosshair)

        #FIT RESULTS
        layout_fits.addWidget(QLabel('2D Gauss fit results'))
        self.gauss_fit_widget = QTableWidget()
        self.gauss_fit_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gauss_fit_widget.setRowCount(5)
        self.gauss_fit_widget.setColumnCount(2)
        self.gauss_fit_widget.setItem(0,0, QTableWidgetItem("x0"))
        self.gauss_fit_widget.setItem(0,1, QTableWidgetItem("1"))
        self.gauss_fit_widget.setItem(1,0, QTableWidgetItem("y0"))
        self.gauss_fit_widget.setItem(1,1, QTableWidgetItem("1"))
        self.gauss_fit_widget.setItem(2,0, QTableWidgetItem("main1_waist"))
        self.gauss_fit_widget.setItem(2,1, QTableWidgetItem("1"))
        self.gauss_fit_widget.setItem(3,0, QTableWidgetItem("main2_waist"))
        self.gauss_fit_widget.setItem(3,1, QTableWidgetItem("1"))
        self.gauss_fit_widget.setItem(4,0, QTableWidgetItem("angle"))
        self.gauss_fit_widget.setItem(4,1, QTableWidgetItem("1"))
        self.gauss_fit_widget.move(0,0)
        layout_fits.addWidget(self.gauss_fit_widget)

        #layout_fits.addStretch()
        layout_fits.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        w = QWidget()
        w.setLayout(layout_split)
        self.setCentralWidget(w)

        self.setWindowTitle("Image Viewer")
        self.resize(1024, 768)
        self.show()

        self.capture_request.emit()

    def change_fit_cb(self, state):
        if state == Qt.Checked:
            self.enable_fit = True
        else:
            self.enable_fit = False

    def save_frame(self):
        image = Image.fromarray(self.current_frame)
        image.save("campi_frame_%d.tiff"%self.frame_counter)

    def test_print(self):
        print('test')

    def px_to_um(self, px):
        return self.pixel_size * float(px)

    def update_centroid_widget(self, results):
        def set_table_entry(i,entry):
            self.centroid_widget.setItem(i,1, QTableWidgetItem(entry))
        set_table_entry(0,"%1.1f"%self.px_to_um(results['x0']))
        set_table_entry(1,"%1.1f"%self.px_to_um(results['y0']))
        set_table_entry(2,"%1.1f"%self.px_to_um(2*np.sqrt(results['main1_var'])))
        set_table_entry(3,"%1.1f"%self.px_to_um(2*np.sqrt(results['main2_var'])))
        set_table_entry(4,"%1.1f"%(results['angle']*180/np.pi))

    def update_gauss_fit_widget(self, results):
        def set_table_entry(i,entry):
            self.gauss_fit_widget.setItem(i,1, QTableWidgetItem(entry))
        set_table_entry(0,"%1.1f"%self.px_to_um(results['x0']))
        set_table_entry(1,"%1.1f"%self.px_to_um(results['y0']))
        set_table_entry(2,"%1.1f"%self.px_to_um(2*results['main1_sigma']))
        set_table_entry(3,"%1.1f"%self.px_to_um(2*results['main2_sigma']))
        set_table_entry(4,"%1.1f"%(results['angle']*180/np.pi))


    def setup_and_start_fitting_thread(self):
        """
        Starts a worker thread for fitting and connects it to the main thread via signals and slots.
        """
        self.ft = QThread()
        self.fw = FitWorker(self.current_frame)
        self.fw.fitted.connect(self.on_fit_success)
        self.fw.fit_error.connect(self.on_fit_error)
        self.fw.moveToThread(self.ft)
        self.fw.finished.connect(self.on_fit_finished)
        self.ft.started.connect(self.fw.run)
        self.ft.start()

    def on_fit_success(self, fit_results):
        # if fitting in fitting thread succeeded, we hand over the fit results and update the GUI
        self.fit_results = fit_results
        print("\nFitting succeeded.\n")
        self.fitting_succeeded = True
        self.update_centroid_widget(self.fit_results['centroid'])
        self.update_gauss_fit_widget(self.fit_results['gauss'])
        #self.parsingLabel.setText('')

    def on_fit_error(self, error):
        self.fitting_succeeded = False
        print("\nParsing error:\n------------------\n%s\n" % str(error))

    def on_fit_finished(self):
        self.ft.quit()
        #self.ft.wait()
        self.capture_request.emit()

    def setup_and_start_camera_thread(self):
        """
        Starts a worker thread for fitting and connects it to the main thread via signals and slots.
        """
        self.ct = QThread()
        self.cam = CameraClient(self.cam_hostname)
        self.cam.captured.connect(self.on_captured)
        self.cam.moveToThread(self.ct)
        self.cam.finished.connect(self.on_cam_disconnected)
        self.capture_request.connect(self.cam.capture)
        self.ct.started.connect(self.cam.connect)
        self.ct.start()

    def on_captured(self, stream):
        self.frame_counter += 1
        self.current_frame = image_from_stream_object(stream)
        self.imv.setImage(self.current_frame.T)
        if self.enable_fit:
            self.setup_and_start_fitting_thread()
        else:
            self.capture_request.emit()

    def on_cam_disconnected(self):
        pass


class FitWorker(QObject):
    finished = pyqtSignal()
    fitted = pyqtSignal(dict)  # signal emitted when fit is completed successfully
    fit_error = pyqtSignal(object)
    fit_timeout = pyqtSignal(int)
    newState = pyqtSignal(int)

    def __init__(self, data):
        QObject.__init__(self)
        self.data = data

    def run(self):
        try:
            #self.timer = QTimer(self)
            #self.timer.setSingleShot(True)
            #self.timer.timeout.connect(self.on_timeout)
            #self.timer.start(10)

            # FITTING
            # centroid
            centroid = get_centroid_info(self.data)

            #gauss fit
            guess = np.array([np.max(self.data),0,\
                centroid['x0'], centroid['y0'],\
                np.sqrt(centroid['main1_var']),np.sqrt(centroid['main2_var']),\
                centroid['angle']])

            gauss_fit = fit_gaussian(self.data, initial_guess=guess)

            self.fitted.emit({'centroid': centroid, 'gauss': gauss_fit})
        except Exception as e:
            self.fit_error.emit(e)

        self.finished.emit()

    @pyqtSlot()
    def on_timeout(self):
        self.fit_timeout.emit(self.timer.remainingTime())
        self.finished.emit()


class CameraClient(QObject):
    finished = pyqtSignal()
    captured = pyqtSignal(object) #signal emitted after image capture and transfer

    def __init__(self, hostname, port=8000):
        QObject.__init__(self)
        self.hostname = hostname
        self.port = port
        self.conn = Client((self.hostname, self.port))

    def connect(self):
        pass

    @property
    def pixel_size(self):
        return self.send_command('get_pixel_size')

    @property
    def resolution(self):
        return self.send_command('get_resolution')

    @property
    def resolution_mode(self):
        return self.send_command('get_resolution_mode')

    @property
    def available_resolution_modes(self):
        return self.send_command('get_available_resolution_modes')

    @pyqtSlot()
    def capture(self):
        frame = self.send_command('capture')
        self.captured.emit(frame)
        return frame

    def send_command(self, command):
        try:
            self.conn.send(command)
            print('Command "', command, '" was sent.')
        except:
            print('Command "', command, '" could not be sent.')

        try:
            answer = self.conn.recv()
            return answer
        except:
            print('No answer for command "', command, '" was received.')

    def disconnect(self):
        self.conn.close()

def run_gui():
    #parse command line args
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--fake', dest='fake', action='store_const', \
                     const=True, default=False, \
                     help='Start fake camera server locally (0.0.0.0).')
    parser.add_argument('-H', '--hostname', dest='hostname', required=True,\
                    help='Host name (IP address) for camera server')
    args = parser.parse_args()

    hostname = args.hostname

    if args.fake:
        from multiprocessing import Process
        hostname = '0.0.0.0'
        def start_fake_server():
            from campi.server.camserver import DummyCamera, CameraServer
            cam = DummyCamera()
            cs = CameraServer(cam)
            cs.listening_loop()
        p = Process(target=start_fake_server)
        p.daemon = True
        p.start()

    app = QApplication(sys.argv)
    cv = CameraViewer(cam_hostname=hostname)
    cv.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()
