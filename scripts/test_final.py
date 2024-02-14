#! /usr/bin/env python
import time
from functools import partial

from red_camera.camera import RedCamera, logging
from red_camera.keypad import KeyPad
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


    # create keypad functions
    keypad = KeyPad()

    increase_fps = partial(camera.increase, RCP_PARAM.FPS)
    decrease_fps = partial(camera.decrease, RCP_PARAM.FPS)
    
    increase_iso = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.ISO_INCREMENT))
    decrease_iso = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.ISO_DECREMENT))

    increase_shutter = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.SHUTTER_INCREMENT))
    decrease_shutter = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.SHUTTER_DECREMENT))

    increase_iris = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.APERTURE_INCREMENT))
    decrease_iris = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.APERTURE_DECREMENT))

    auto_wb = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.AUTO_WB))
    increase_wb = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.COLOR_TEMPERATURE_INCREMENT))
    decrease_wb = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.COLOR_TEMPERATURE_DECREMENT))

    playback_toggle = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.PLAYBACK_PLAY_PAUSE_TOGGLE))

    record_toggle = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.RECORD_TOGGLE))

    pre_record_toggle = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.PRE_RECORD_ENABLE_TOGGLE))
    
    start_af = partial(camera.send, RCPSet(RCP_PARAM.KEYACTION, action=RCP_KEYACTION.START_AF))

    keypad_functions = [
        [increase_fps,  increase_iso,       increase_shutter,   increase_iris],
        [decrease_fps,  decrease_iso,       decrease_shutter,   decrease_iris],
        [increase_wb,   playback_toggle,    auto_wb,            pre_record_toggle],
        [decrease_wb,   start_af,           None,               record_toggle]
    ]

    logging.info('Press keypad button...')

    while True:
        r,c = keypad.read()

        if r is not None and c is not None:
            f = keypad_functions[r][c]
            if callable(f): 
                logging.warning(f'Button [{r},{c}] pressed!')
                f()
            else:
                logging.warning(f'Button [{r},{c}] pressed but has no function!')

        time.sleep(0.01)


if __name__ == "__main__":
    main()