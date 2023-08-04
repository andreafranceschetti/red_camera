#! /usr/bin/env python

from red_camera.camera import RedCamera
from red_camera.connections.websocket import RedCameraWebSocketConnection
from red_camera.rcp import *

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