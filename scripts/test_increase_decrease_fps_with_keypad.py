#! /usr/bin/env python
import time
from functools import partial

from red_camera.camera import RedCamera, logging
from red_camera.keypad import KeyPad
from red_camera.connections.wifi import WifiRedCameraConnection
from red_camera.rcp import RCP_PARAM

def main():

    wifi = WifiRedCameraConnection()
    wifi.open('ws://192.168.1.1:9998')



    camera = RedCamera(connection=wifi)
    camera.initialize()
    camera.get_camera_info()

    # get all the necessary parameters
    camera.get_list(RCP_PARAM.FPS)


    # create keypad functions
    keypad = KeyPad()
    
    increase_fps = partial(camera.increase, RCP_PARAM.FPS)
    decrease_fps = partial(camera.decrease, RCP_PARAM.FPS)

    keypad_functions = [
        [increase_fps, None, None, None],
        [decrease_fps, None, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]

    logging.info('Press keypad button...')

    while True:
        r,c = keypad.read()

        if r and c:
            f = keypad_functions[r][c]
            if callable(f): 
                f()
            else:
                logging.warn(f'Button [{r},{c}] has no function!')

        time.sleep(0.01)


if __name__ == "__main__":
    main()