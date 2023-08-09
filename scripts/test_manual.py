#! /usr/bin/env python

from red_camera.camera import RedCamera
from red_camera.connections.wifi import WifiRedCameraConnection
from red_camera.rcp import *
from time import sleep

def main():

    wifi = WifiRedCameraConnection()
    wifi.open('ws://192.168.1.1:9998')

    camera = RedCamera(connection=wifi)
    camera.initialize()
    camera.get_camera_info()

    while True:
        sleep(0.05)

        char = input()

        if char == 'iso+': # arrow up
            camera.send(iso_plus)
        elif char == 'iso-': 
            camera.send(iso_minus)
        elif char == 'sub_fps':
            camera.send(RCPSubscribe(RCP_PARAM.FPS))
        elif char == 'fps+':
            camera.send(RCPSetRelative(RCP_PARAM.FPS, 30))
        elif char == 'fps-':
            camera.send(RCPSetRelative(RCP_PARAM.FPS, -30))
        elif char == 'fps=60':
            camera.send(RCPSet(RCP_PARAM.FPS, 30030))
        elif char == 'getfps':
            camera.send(RCPGetList(RCP_PARAM.FPS))
        elif char == 'getiso':
            camera.send(RCPGetList(RCP_PARAM.ISO))
        elif char == 'aon':
            camera.send(af_on)
        elif char == 'aoff':
            camera.send(af_off)
        elif char == 'getaf':
            camera.send(RCPGetList(RCP_PARAM.AUTOFOCUS))
        elif char == 'getape':
            camera.send(RCPGetList(RCP_PARAM.APERTURE))
        elif char == 'ape+':
            camera.send(RCPSetListRelative(RCP_PARAM.AUDIO_EXTERNAL_LEFT_GAIN, +1))
        elif char == 'ape-':
            camera.send(RCPSetListRelative(RCP_PARAM.AUDIO_EXTERNAL_LEFT_GAIN, -1))
        elif char == 'wb+':
            camera.send(RCPSetListRelative(RCP_PARAM.COLOR_TEMP, +1))
        elif char == 'wb-':
            camera.send(RCPSetListRelative(RCP_PARAM.COLOR_TEMP, -1))



if __name__ == "__main__":
    main()