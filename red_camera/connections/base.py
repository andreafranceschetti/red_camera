from abc import ABC, abstractmethod
from red_camera.rcp import RCPMessage
import logging


logging.basicConfig(level=logging.INFO)

from time import sleep

class RedCameraConnection(ABC):

    @abstractmethod
    def open(self, *args):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def send(self, message : RCPMessage):
        pass

    @abstractmethod
    def recv(self, timeout=None) -> RCPMessage:
        pass

