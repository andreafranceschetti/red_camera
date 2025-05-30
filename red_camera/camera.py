from threading import Thread
from time import sleep
from typing import Dict
import logging

from red_camera.connections.base import RedCameraConnection
from red_camera.rcp import *


logging.basicConfig(level=logging.INFO)

class RedCamera:


    def __init__(self, connection: RedCameraConnection) -> None:
        self.connection = connection
        self.available_settings : dict = {}
        self.info : dict = {}
        self.custom_available_settings : Dict[str, RCPParamList] = {}
        self.initialized = False

    def __receive_rcp(self):
        """rcp receiving thread"""
        while True:
            msg = self.connection.recv()
            logging.debug(f'*** Camera rx  <<<<< : {msg.data}')

            if msg.type == RCP_TYPE.RCP_CONFIG:
                logging.info('Camera initialized')
                self.initialized = True
            elif msg.type == RCP_TYPE.RCP_CUR_TYPES:
                logging.debug('received camera available settings')
                self.available_settings = msg.data
            elif msg.type == RCP_TYPE.RCP_CUR_CAM_INFO:
                self.info = msg.data
                logging.info(self.info)
            elif msg.type == RCP_TYPE.RCP_CUR_LIST:
                cur = msg.data['list']['cur']
                param_list = [RCPParam(param['num'], param['str']) for param in msg.data['list']['data']]
                self.custom_available_settings['RCP_PARAM_' + msg.id] = RCPParamList(cur=cur, param_list=param_list)
            elif msg.type == RCP_TYPE.RCP_CUR_INT:
                param_id = msg.id
                param_value = msg.data['cur']
                logging.info(f'Parameter {param_id} set to {param_value }')
            elif msg.type == RCP_TYPE.RCP_CUR_STR:
                param_id = msg.id
                param_value = msg.data['display']
                logging.info(f'Parameter {param_id} set to {param_value }')

    def send(self, message: RCPMessage) -> None:
        logging.debug(f'*** Camera tx >>>>>>  {message.data}')
        self.connection.send(message)
        

    def _set_value(self, param_id: RCP_PARAM, offset:int):

        if not self.initialized:
            logging.warning('Camera is not initialized')
            return

        for _ in range(3):
            try:
                available_param_list = self.custom_available_settings[param_id]
                break
            except KeyError:
                logging.warn(f'Parameter {param_id} not found in database... Requesting all the available ones')
                self.get_list(param_id)
                sleep(0.1)

        current_value_idx = available_param_list.cur
        current_value = available_param_list.param_list[current_value_idx].string
        
        next_cur = current_value_idx + offset

        if next_cur > len(available_param_list.param_list):
            logging.warn(f'Parameter {param_id} already at maximum value {current_value}!')
            return
        if next_cur < 0:
            logging.warn(f'Parameter {param_id} already at minimum value {current_value}!')
            return
        
        next_value = available_param_list.param_list[next_cur].number
        self.connection.send(RCPSet(param_id, value=next_value))


    def initialize(self) -> bool:
        """starts the receiving thread and s
        ends a rcp_config messaget to initialize the camera json protocol
        """

        self.rcp_thread = Thread(target=self.__receive_rcp)
        # self.keypad_thread = Thread(target=self.__receive_keypad)

        self.rcp_thread.start()
        # self.keypad_thread.start()

        logging.info('Initializing camera...')
        while not self.initialized:
            self.connection.send(RCPConfig())
            self.connection.send(RCPGetTypes())
            sleep(0.1)

        return self.initialized
    
    def get_camera_info(self) -> None:
        """gets the camera infos"""
        if not self.initialized:
            logging.warning('Camera is not initialized')
            return

        self.connection.send(RCPGet(RCP_PARAM.CAMERA_INFO))

    def get_list(self, param_id:RCP_PARAM):
        """sends rcp_get_list for a given parameter"""
        if not self.initialized:
            logging.warning('Camera is not initialized')
            return
        self.connection.send(RCPGetList(param_id))

    def increase(self, param_id: RCP_PARAM, step = 1):
        self._set_value(param_id, step)
    
    def decrease(self, param_id: RCP_PARAM, step = -1):
        self._set_value(param_id, step)
