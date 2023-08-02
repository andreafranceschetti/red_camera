from gpiozero import Button
from websockets.sync.client import connect, ClientConnection
import json
from time import sleep
from typing import List
from enum import Enum


class RCPMessage:
    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def type(self) -> str:
        return self.data["type"]

    @property
    def id(self) -> str:
        return self.data["id"]

    def to_json(self) -> str:
        return json.dumps(self.data)


class RCPGetTypes(RCPMessage):

    def __init__(self) -> None:

        self.data = {
            "type": "rcp_get_types"
        }

class RCPConfig(RCPMessage):

    def __init__(self) -> None:

        self.data = {
            "type": "rcp_config",
            "strings_decoded": 0,
            "json_minified": 1,
            "include_cacheable_flags": 0,
            "encoding_type": "legacy",
            "client": {"name": "My Awesome Control App", "version": "1.42"},
        }

class RCPSet(RCPMessage):

    def __init__(self, param_id:str, value=None, x=None, y=None, width=None, height=None, action=None, held=None, argument=None ) -> None:
        self.data = {
            "type":"rcp_set",
            "id": param_id,
        }

        if value:
            self.data['value'] = value
        if x:
            self.data['x'] = x
        if y: 
            self.data['y'] = y
        if width:
            self.data['width'] = width
        if height: 
            self.data['height'] = height
        if action:
            self.data['action'] =action
        if argument:
            self.data['argument'] = argument

class RCPSetRelative(RCPMessage):

    def __init__(self, param_id:str, offset) -> None:
        self.data = {
            "type":"rcp_set_relative",
            "id": param_id,
            "offset": offset
        }

class RCPSetListRelative(RCPMessage):

    def __init__(self, param_id:str, offset:int) -> None:
        self.data = {
            "type":"rcp_set_list_relative",
            "id": param_id,
            "offset": offset
        }

class RCPGetList(RCPMessage):

    def __init__(self, param_id:str) -> None:
        self.data = {
            "type":"rcp_get_list",
            "id": param_id,
        }

class RedCamera:

    websocket : ClientConnection = None
    available_settings : dict = {}

    def connect(self, uri:str) -> bool:

        while (not self.websocket):
            try:
                self.websocket = connect(uri)
                return True
            except Exception as e:
                print(f'Cannot connect to websocket {uri} due to {e}')
                sleep(1)

    def send(self, message: RCPMessage):
        self.websocket.send(message.to_json())
        return self.recv(timeout=0.1)

    def recv(self, timeout = 0.1) -> RCPMessage:
        try:
            data = json.loads(self.websocket.recv(timeout=timeout))
        except TimeoutError:
            return None 
        return RCPMessage(data)
    
    def initialize(self) -> bool:
        resp = self.send(RCPConfig())

        if resp.type == RCPConfig().type:
            return True
        
        return False
    
    def set(self, rcp_set: RCPSet):
        # should check if this param id is in available settings
        self.send(rcp_set)
    
    def retrieve_available_config(self):
        available_settings = self.send(RCPGetTypes())
        self.available_settings = available_settings.data
        print(self.available_settings)

class KeyPadCommands(Enum):

    ZOOM = 0
    AUTOFOCUS = 1

iso_plus = RCPSetListRelative("ISO", +1)
iso_minus = RCPSetListRelative("ISO", -1)

fps_plus  = RCPSetListRelative("SENSOR_FRAME_RATE", +1)
fps_minus = RCPSetListRelative("SENSOR_FRAME_RATE", -1)

class KeyPad:


    def __init__(self) -> None:
        self.row = [Button(n) for n in range(0,4)]
        self.col = [Button(n) for n in range(5,9)]



        self.config = [
            [iso_plus, iso_minus, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
    ]
    

    def check(self):
        for r in self.row:
            for c in self.col:
                if r.is_pressed and c.is_pressed:
                    return r, c
        
        return None, None
    

                    
get_fps = RCPGetList("SENSOR_FRAME_RATE")
get_iso = RCPGetList("ISO")



def main():

    # websocket init
    camera = RedCamera()
    camera.connect('ws://192.168.1.1:9998')
    camera.initialize()
    camera.retrieve_available_config()

    # keypad = KeyPad()

    # gpio reading loop
    while(True):
        # sleep(0.05)

        char = input()

        if char == '\x1b[A': # arrow up
            camera.send(iso_plus)
            # print(camera.recv().data)
            # print(camera.recv().data)
            # print(camera.recv().data)
        elif char == '\x1b[B': 
            camera.send(iso_minus)
            # print(camera.recv().data)
            # print(camera.recv().data)
            # print(camera.recv().data)
        elif char == 'e':
            camera.send(fps_plus)
            # print(camera.recv().data)
        elif char == 'g':
            msg = camera.send(get_fps)
            print(msg.data)
        elif char == 'i':
            camera.send(get_iso)
            print(camera.recv().data)

        # c,r = keypad.check()        

        # if c is not None and r is not None:
            # camera.send(keypad.config[r][c])
            # sleep(0.1)


if __name__ == "__main__":
    main()
