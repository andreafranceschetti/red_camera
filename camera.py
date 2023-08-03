from websockets.sync.client import connect, ClientConnection
from threading import Thread
from time import sleep
import json

from rcp import *

class RedCamera:

    websocket : ClientConnection = None
    available_settings : dict = {}
    info : dict = {}

    def connect(self, uri:str) -> bool:

        while (not self.websocket):
            try:
                self.websocket = connect(uri)
                receive_thread = Thread(target=self.__receive)
                receive_thread.start()
                return True
            except Exception as e:
                print(f'Cannot connect to websocket {uri} due to {e}')
                sleep(1)
    
    def __receive(self):
        while True:
            msg = self.recv()

            if msg.type == RCP_TYPE.RCP_CONFIG:
                print('Camera initialized')
            elif msg.type == RCP_TYPE.RCP_CUR_TYPES:
                print('received camera available settings')
                self.available_settings = msg.data
            elif msg.type == RCP_TYPE.RCP_CUR_CAM_INFO:
                self.info = msg.data
                print(self.info)
            else:
                print(msg.data)

    def send(self, message: RCPMessage) -> None:
        self.websocket.send(message.to_json())

    def recv(self, timeout = None) -> RCPMessage:
        try:
            data = json.loads(self.websocket.recv(timeout=timeout))
        except TimeoutError:
            return None 
        return RCPMessage(data)
    
    def initialize(self) -> bool:
        self.send(RCPConfig())
    
    def retrieve_available_config(self):
        self.send(RCPGetTypes())

    def get_info(self) -> None:
        self.send(RCPGet(RCP_PARAM.CAMERA_INFO))
