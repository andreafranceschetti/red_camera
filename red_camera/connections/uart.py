import logging
import time
import json

from typing import Optional

from serial import Serial

from red_camera.rcp import RCPMessage
from red_camera.connections.base import RedCameraConnection

class UartSerialRedCameraConnection(RedCameraConnection):

    def __init__(self, port: str = '/dev/ttyACM0') -> None:
        self.port = port
        self.serial = Serial(port, 115200)

    def open(self):
        while not self.serial.is_open:
            try:
                self.serial.open()
            except Exception as e:
                logging.error(f'Cannot open port {self.port} due to {e}, retrying in 1 seconds')
                time.sleep(1)
    
    def close(self):
        self.serial.close()

    def send(self, message:RCPMessage):
        self.serial.write(message.to_json().encode())

    def recv(self) -> Optional[RCPMessage]:
        """if timeout is None, this is blocking until a new message is received"""
        try:
            while True:
                if self.serial.in_waiting > 0:
                    data = json.loads(self.serial.readall())
                    self.serial.reset_input_buffer()
                    return RCPMessage(data)
                time.sleep(0.01)

        except TimeoutError:
            logging.error('timeout error!')
            return None 
        except Exception as e:
            logging.error(f'{e}')
            return None