from camera import RedCamera
from rcp import *
from time import sleep


def main():

    camera = RedCamera()
    camera.connect('ws://192.168.1.1:9998')
    camera.initialize()
    camera.get_info()
    camera.retrieve_available_config()

    # keypad = KeyPad()

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



    # gpio reading loop
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
        # c,r = keypad.check()        

        # if c is not None and r is not None:
            # camera.send(keypad.config[r][c])
            # sleep(0.1)


if __name__ == "__main__":
    main()