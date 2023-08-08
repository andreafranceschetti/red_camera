#! /usr/bin/env python

from red_camera.camera import RedCamera
from red_camera.connections.wifi import RedCameraWifiConnection
from red_camera.rcp import *
from time import sleep

# this application allows the 

def main():
    wifi = RedCameraWifiConnection()
    wifi.open('ws://192.168.1.1:9998')

    camera = RedCamera(connection=wifi)
    camera.initialize()
    camera.get_camera_info()

    while True:
        sleep(0.5)

        rcp_msg = input('Choose rcp message: ').lower()
        rcp_param_id = input('Choose a param id: ').upper()

        if  'relative' in rcp_msg:

            rcp_param_offset = input('Choose a param offset: ')
            msg = RCPMessage({
                'type' : rcp_msg,
                'id': rcp_param_id,
                'offset': rcp_param_offset
            })

        else:

            rcp_param_value = input('Choose a param value: ')
            msg = RCPMessage({
                'type' : rcp_msg,
                'id': rcp_param_id,
                'value': rcp_param_value
            })



        camera.send(msg)

if __name__ == "__main__":
    main()