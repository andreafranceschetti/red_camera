#! /usr/bin/env python

from red_camera.camera import RedCamera
from red_camera.connections.wifi import WifiRedCameraConnection
from red_camera.rcp import *

def main():

    wifi = WifiRedCameraConnection()
    wifi.open('ws://192.168.1.1:9998')

    camera = RedCamera(connection=wifi)
    camera.initialize()
    camera.get_camera_info()

    # get all the necessary parameters
    camera.get_list(RCP_PARAM.FPS)


    while True:

        c = input('Increase/decrease FPS with fps+ or fps- (exit for termination):')

        if c == 'fps+':
            camera.increase(RCP_PARAM.FPS)
        elif c == 'fps-':
            camera.decrease(RCP_PARAM.FPS)
        elif c == 'exit':
            return
        else:
            print(f'unknown command {c}')


if __name__ == "__main__":
    main()