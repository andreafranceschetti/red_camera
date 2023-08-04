from red_camera.camera import RedCamera
from red_camera.connections.websocket import RedCameraWebSocketConnection
from red_camera.rcp import *
from time import sleep

# shutter > EXPOSURE_ANGLE
# fps > SENSOR_FRAME_RATE
# iso > ISO


def general_message():

    camera = RedCamera()
    camera.connect('ws://192.168.1.1:9998')
    camera.initialize()
    camera.get_info()
    camera.retrieve_available_config()
    
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



        camera._send(msg)

def custom_set():
    camera = RedCamera()
    camera.connect('ws://192.168.1.1:9998')
    camera.initialize()
    camera.get_info()
    camera.retrieve_available_config()
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

        camera._send(RCPSet(param_id='RCP_PARAM_' + param_id, value=param_value))

def custom_command():
    camera = RedCamera()
    camera.connect('ws://192.168.1.1:9998')
    camera.initialize()
    camera.get_info()
    camera.retrieve_available_config()
    while True:
        sleep(0.05)

        char = input()

        if char == 'iso+': # arrow up
            camera._send(iso_plus)
        elif char == 'iso-': 
            camera._send(iso_minus)
        elif char == 'sub_fps':
            camera._send(RCPSubscribe(RCP_PARAM.FPS))
        elif char == 'fps+':
            camera._send(RCPSetRelative(RCP_PARAM.FPS, 30))
        elif char == 'fps-':
            camera._send(RCPSetRelative(RCP_PARAM.FPS, -30))
        elif char == 'fps=60':
            camera._send(RCPSet(RCP_PARAM.FPS, 30030))
        elif char == 'getfps':
            camera._send(RCPGetList(RCP_PARAM.FPS))
        elif char == 'getiso':
            camera._send(RCPGetList(RCP_PARAM.ISO))
        elif char == 'aon':
            camera._send(af_on)
        elif char == 'aoff':
            camera._send(af_off)
        elif char == 'getaf':
            camera._send(RCPGetList(RCP_PARAM.AUTOFOCUS))
        elif char == 'getape':
            camera._send(RCPGetList(RCP_PARAM.APERTURE))
        elif char == 'ape+':
            camera._send(RCPSetListRelative(RCP_PARAM.AUDIO_EXTERNAL_LEFT_GAIN, +1))
        elif char == 'ape-':
            camera._send(RCPSetListRelative(RCP_PARAM.AUDIO_EXTERNAL_LEFT_GAIN, -1))
        elif char == 'wb+':
            camera._send(RCPSetListRelative(RCP_PARAM.COLOR_TEMP, +1))
        elif char == 'wb-':
            camera._send(RCPSetListRelative(RCP_PARAM.COLOR_TEMP, -1))


def main():

    websocket = RedCameraWebSocketConnection()
    websocket.open('ws://192.168.1.1:9998')

    camera = RedCamera(connection=websocket)
    camera.initialize()
    camera.get_camera_info()

    # get all the necessary parameters
    camera.get_list(RCP_PARAM.FPS)

    # increase/decrease them
    # camera.decrease(RCP_PARAM.FPS)
    camera.increase(RCP_PARAM.FPS)
    # camera.decrease(RCP_PARAM.FPS)




if __name__ == "__main__":
    main()