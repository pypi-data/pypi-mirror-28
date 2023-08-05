import io
import sys
import socket
import struct
import time
from PIL import Image
import numpy as np
import multiprocessing as mp
from multiprocessing.connection import Listener, Client
import skimage.io
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

class PinoirCamera():
    def __init__(self):
        self.init_cam()
        self.capture_format = 'jpeg' # jpeg, yuv, png, ...
        self._available_resolutions = [(3280,2464), (1640,1232),(640,480)] # available resolutions that use the full sensor area
        self._available_pixel_sizes = [1.12, 2.24, 1.12*5.125] # um/px
        self.available_resolution_modes = {
                'full': {'resolution': self._available_resolutions[0], 'pixel_size': self._available_pixel_sizes[0]},
                'half': {'resolution': self._available_resolutions[1], 'pixel_size': self._available_pixel_sizes[1]},
                'small': {'resolution': self._available_resolutions[2], 'pixel_size': self._available_pixel_sizes[2]}
                }
        self.resolution_mode = 'half'

    def init_cam(self):
        import picamera
        self.cam = picamera.PiCamera()

    @property
    def resolution_mode(self):
        return self._resolution_mode

    @resolution_mode.setter
    def resolution_mode(self, mode):
        if mode in self.available_resolution_modes:
            self._resolution_mode = mode
            self.cam.resolution = self.available_resolution_modes[self._resolution_mode]['resolution']

    @property
    def resolution(self):
        return self.available_resolution_modes[self.resolution_mode]['resolution']

    @property
    def pixel_size(self):
        return self.available_resolution_modes[self.resolution_mode]['pixel_size']

    def capture(self):
        """ take and return one image in the specified format """
        stream = io.BytesIO()
        self.cam.capture(stream,\
            use_video_port=True,\
            format=self.capture_format)
        stream.seek(0)
        return stream

class DummyCamera(PinoirCamera):
    def __init__(self):
        self.init_cam()
        self.capture_format = 'jpeg' # jpeg, yuv, png, ...
        self._available_resolutions = [(3280,2464), (1640,1232),(640,480)] # available resolutions that use the full sensor area
        self._available_pixel_sizes = [1.12, 2.24, 1.12*5.125] # um/px
        self.available_resolution_modes = {
                'full': {'resolution': self._available_resolutions[0], 'pixel_size': self._available_pixel_sizes[0]},
                'half': {'resolution': self._available_resolutions[1], 'pixel_size': self._available_pixel_sizes[1]},
                'small': {'resolution': self._available_resolutions[2], 'pixel_size': self._available_pixel_sizes[2]}
                }
        self.resolution_mode = 'half'

    def init_cam(self):
        pass

    @property
    def resolution_mode(self):
        return self._resolution_mode

    @resolution_mode.setter
    def resolution_mode(self, mode):
        if mode in self.available_resolution_modes:
            self._resolution_mode = mode

    def capture(self):
        resX = self.resolution[0]
        resY = self.resolution[1]
        xy = np.meshgrid(range(resX), range(resY))
        frame = gaussian2D(xy,1,0.0,500+np.random.randint(25),600+np.random.randint(50),10,20,0.1).reshape(resY, resX)
        data = (frame + 0.2*np.random.rand(resY,resX))
        data = ((data - data.min()) / (data.ptp() / 255)).astype(np.uint8) # map the data range to 0 - 255
        image = Image.fromarray(data)
        stream = BytesIO()
        image.save(stream,format="JPEG")
        sleep(0)
        #stream.seek(0)
        return stream


class CameraServer():
    def __init__(self, cam):
        self.address = ('0.0.0.0', 8000)
        self.cam = cam
        self.listener = Listener(self.address)
        self.look_for_client()

    def listening_loop(self):
        i=0
        while True:
            try:
                cmd = self.conn.recv()
                self.print('received command: '+ cmd)
            except:
                self.print('No command from client received. Client disconnected?')
                self.disconnect()
                self.look_for_client()

            if cmd == 'capture':
                frame = self.cam.capture()
                self.send_to_client(frame, 'frame %d'%i)
                i+=1

            elif cmd == 'get_pixel_size':
                self.send_to_client(self.cam.pixel_size, 'camera pixel size')

            elif cmd == 'get_resolution':
                self.send_to_client(self.cam.resolution, 'camera resolution')

            elif cmd == 'get_resolution_mode':
                self.send_to_client(self.cam.resolution_mode, 'camera resolution mode')

            elif cmd == 'get_available_resolution_modes':
                self.send_to_client(self.cam.available_resolution_modes, 'available camera resolution modes')


    def look_for_client(self):
        self.print('Camera server is accepting client connections now')
        self.conn = self.listener.accept()
        self.print('Connection to client established.')

    def send_to_client(self, content, description=''):
        try:
            self.conn.send(content)
            self.print(description + ' was sent')
        except:
            self.print(description + ' could not be sent. Client disconnected?')
            self.look_for_client()

    def disconnect(self):
        self.conn.close()

    def print(self, text):
        color = '\033[94m'
        endc = '\033[0m'
        print(color + text + endc)


def start():
    parser = argparse.ArgumentParser(description='Parse arguments for camera server script.')
    parser.add_argument('--fake', dest='fake', action='store_const', \
                     const=True, default=False, \
                     help='use fake camera as server feed instead of picamera')
    args = parser.parse_args()

    if args.fake:
        cam = DummyCamera()
    else:
        cam = PinoirCamera()

    cs = CameraServer(cam)
    cs.listening_loop()
    
if __name__ == "__main__":
    start()
