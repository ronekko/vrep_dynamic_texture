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


if __name__ == '__main__':
    try:
        client_id
    except NameError:
        client_id = -1
    e = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot_wait)
    vrep.simxFinish(-1)
    client_id = vrep.simxStart(six.b('127.0.0.1'), 19998, True, True, 5000, 5)

    assert client_id != -1, 'Failed to connect to the V-rep server'

    e = vrep.simxStartSimulation(client_id, vrep.simx_opmode_oneshot_wait)
    # Handles of body and wheels
    e, vision = vrep.simxGetObjectHandle(client_id, six.b('Vision_sensor'),
                                         vrep.simx_opmode_oneshot_wait)

    for i in range(10000):
        print(i)
        image_width, image_height = 128, 128
#        image = np.random.randint(0, 255, size=(128, 128, 3), dtype=np.uint8)
        theta = np.pi * float(i) / 60
        r = (np.sin(theta / 10) + 1) / 2.0
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        fig = Figure(figsize=(image_height / 100.0, image_width / 100.0))
        ax = fig.gca()
        ax.plot(x, y, '.', markersize=20)
        ax.set_ylim(-1, 1)
        ax.set_xlim(-1, 1)
        ax.set_aspect('equal', adjustable='box')
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        image = np.fromstring(canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape((image_height, image_width, 3))

        if image.ndim == 3:
            is_color = 0
        elif image.ndim == 2:
            is_color = 1
        else:
            raise ValueError('"image" must be np.ndarray of (H, W, C)-shaped'
                             '3D array (i.e. color) or (H, W)-shaped 2D array'
                             '(i.e. gray scale)')
        serial_image = image.ravel()
        e = vrep.simxSetVisionSensorImage(client_id, vision, serial_image,
                                          is_color, vrep.simx_opmode_oneshot)
        vrep.simxSynchronousTrigger(client_id)

    e = vrep.simxStopSimulation(client_id, vrep.simx_opmode_oneshot_wait)
