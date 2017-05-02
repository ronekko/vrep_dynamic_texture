# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 19:46:21 2017

@author: sakurai
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
import six
import vrep


class Vrep(object):
    def __init__(self, address='127.0.0.1', port=19998,
                 wait_until_connected=True,
                 do_not_reconnect_once_disconnected=True, time_out_in_ms=5000,
                 comm_thread_cycle_in_ms=5):
        '''See http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm#simxStart
        '''

        vrep.simxStopSimulation(-1, vrep.simx_opmode_oneshot_wait)
        vrep.simxFinish(-1)
        client_id = vrep.simxStart(six.b(address), port, wait_until_connected,
                                   do_not_reconnect_once_disconnected,
                                   time_out_in_ms, comm_thread_cycle_in_ms)
        assert client_id != -1, 'Failed to connect to the V-rep server'

        vrep.simxStartSimulation(client_id, vrep.simx_opmode_oneshot_wait)
        self.client_id = client_id
        self.handles = {}

    def register_handle(self, handle_name):
        _, handle = vrep.simxGetObjectHandle(
            self.client_id, six.b(handle_name), vrep.simx_opmode_oneshot_wait)
        self.handles[handle_name] = handle

    def set_image(self, handle_name, image):
        if image.ndim == 3:
            is_color = 0
        elif image.ndim == 2:
            is_color = 1
        else:
            raise ValueError('`image` must be np.ndarray of (H, W, C)-shaped'
                             '3D array (i.e. color) or (H, W)-shaped 2D array'
                             '(i.e. gray scale)')
        serial_image = image.ravel()
        vrep.simxSetVisionSensorImage(
            self.client_id, self.handles[handle_name], serial_image,
            is_color, vrep.simx_opmode_oneshot)

    def send(self):
        vrep.simxSynchronousTrigger(self.client_id)


if __name__ == '__main__':
    # Resolution of image. These must correspond to `Resolution X / Y` of
    # vision sensor (Scene Object Properties -> Main properties)
    image_width, image_height = 100, 314

    simulator = Vrep()
    vision1 = 'Vision_sensor'  # name of the vision sensor in V-rep
    simulator.register_handle(vision1)

    for i in range(10000):
        # example 1: random noise
        image = np.random.randint(
            0, 255, size=(image_width, image_height, 3), dtype=np.uint8)

#        # example 2: moving ball
#        theta = np.pi * float(i) / 60
#        r = (np.sin(theta / 4) + 1) / 2.0
#        x = r * np.cos(theta)
#        y = r * np.sin(theta)
#        fig = Figure(figsize=(image_height / 100.0, image_width / 100.0))
#        ax = fig.gca()
#        ax.plot(x, y, '.', markersize=20)
#        ax.set_ylim(-1, 1)
#        ax.set_xlim(-1, 1)
#        ax.set_aspect('equal', adjustable='box')
#        canvas = FigureCanvasAgg(fig)
#        canvas.draw()
#        image = np.fromstring(canvas.tostring_rgb(), dtype='uint8')
#        image = image.reshape((image_height, image_width, 3))

        simulator.set_image(vision1, image)
        simulator.send()  # advance 1 time-step in the simulator
        print(i)
