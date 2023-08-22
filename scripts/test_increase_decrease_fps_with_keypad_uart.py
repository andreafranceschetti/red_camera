#! /usr/bin/env python
import time
from functools import partial

from red_camera.camera import RedCamera, logging
from red_camera.keypad import KeyPad
from red_camera.connections.uart import UartSerialRedCameraConnection
from red_camera.rcp import *

def main():

    uart = UartSerialRedCameraConnection()
    uart.open()

    camera = RedCamera(connection=uart)
    camera.initialize()
    camera.get_camera_info()

    # get all the necessary parameters
    camera.get_list(RCP_PARAM.FPS)


    # create keypad functions
    keypad = KeyPad()

    increase_fps = partial(camera.increase, RCP_PARAM.FPS)
    decrease_fps = partial(camera.decrease, RCP_PARAM.FPS)
    
    increase_iso = partial(camera.send, RCPSetListRelative(RCP_PARAM.ISO, +1))
    decrease_iso = partial(camera.send, RCPSetListRelative(RCP_PARAM.ISO, -1))

    keypad_functions = [
        [increase_fps, increase_iso, None, None],
        [decrease_fps, decrease_iso, None, None],
        [None, None, None, None],
        [None, None, None, None]
    ]

    logging.info('Press keypad button...')

    while True:
        r,c = keypad.read()

        if r and c:
            f = keypad_functions[r][c]
            if callable(f): 
                logging.warning(f'Button [{r},{c}] pressed!')
                f()
            else:
                logging.warning(f'Button [{r},{c}] pressed but has no function!')

        time.sleep(0.01)


if __name__ == "__main__":
    main()