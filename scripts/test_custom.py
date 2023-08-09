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
        sleep(1)
        available_parameters = [param.upper() for param in camera.available_settings.keys()]
        available_parameters.sort()
        param_id_name = input(f'Choose the parameter to change from {available_parameters}\n -------------------------------------------------\n').lower()

        
        try:
            available_ids = list(camera.available_settings[param_id_name])
        except KeyError:
            print(f'parameter {param_id_name.upper()} not available, try again')
            continue

        param_id = param_id_name.upper()

        available_ids.sort() 
        param_value_name = input(f'Select one of the following available values: {available_ids}\n').upper()

        try:
            param_value = camera.available_settings[param_id_name][param_value_name]
        except KeyError:
            print('Parameter value not available!')
            continue

        print(f'Sending rcp_set with id= RCP_PARAM_{param_id}, value={param_value}...\n')

        camera.send(RCPSet(param_id='RCP_PARAM_' + param_id, value=param_value))

if __name__ == "__main__":
    main()