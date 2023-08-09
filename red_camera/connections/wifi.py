import logging
import time
import json

from websockets.sync.client import connect, ClientConnection

from red_camera.rcp import RCPMessage
from red_camera.connections.base import RedCameraConnection

class WifiRedCameraConnection(RedCameraConnection):

    websocket : ClientConnection = None

    def open(self, uri:str):
        while (not self.websocket):
            try:
                self.websocket = connect(uri)
                return True
            except Exception as e:
                logging.error(f'Cannot connect to websocket {uri} due to {e}, retrying in 1 seconds')
                time.sleep(1)
    
    def close(self):
        if self.websocket:
            self.websocket.close()

    def send(self, message:RCPMessage):
        self.websocket.send(message.to_json())

    def recv(self, timeout = None) -> RCPMessage:
        """if timeout is None, this is blocking until a new message is received"""
        try:
            data = json.loads(self.websocket.recv(timeout=timeout))
        except TimeoutError:
            logging.error('timeout error!')
            return None 
        except Exception as e:
            logging.error(f'{e}')
            return None
        return RCPMessage(data)

# class RedCameraSerialConnection ??