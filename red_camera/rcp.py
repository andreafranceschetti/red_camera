import json 
from typing import List

class RCP_PARAM:
    FPS = "RCP_PARAM_SENSOR_FRAME_RATE"
    ISO = "RCP_PARAM_ISO"
    AUTOFOCUS = "RCP_PARAM_AF_ENABLE"
    COLOR_TEMP = "RCP_PARAM_COLOR_TEMPERATURE"
    APERTURE = "RCP_PARAM_APERTURE"
    AUDIO_EXTERNAL_LEFT_GAIN = 'RCP_PARAM_AUDIO_EXTERNAL_LEFT_GAIN'
    FAN_MODE = 'RCP_PARAM_FAN_MODE'
    CAMERA_INFO = 'RCP_PARAM_CAMERA_INFO'
    SHUTTER_ANGLE = 'RCP_PARAM_EXPOSURE_ANGLE'
    EXPOSURE_SHUTTER_ANGLE = 'RCP_PARAM_EXPOSURE_ANGLE'
    EXPOSURE_SHUTTER_DISPLAY = 'RCP_PARAM_EXPOSURE_DISPLAY'
    EXPOSURE_SHUTTER_SPEED = 'RCP_PARAM_EXPOSURE_INTEGRATION_TIME'
    KEYACTION = 'KEYACTION'

class RCP_TYPE:
    RCP_GET = 'rcp_get'
    RCP_GET_TYPES = 'rcp_get_types'
    RCP_CUR_TYPES = 'rcp_cur_types'
    RCP_CUR_LIST = 'rcp_cur_list'
    RCP_GET_LIST = 'rcp_get_list'
    RCP_CONFIG = 'rcp_config'
    RCP_SET = 'rcp_set'
    RCP_CUR_INT = 'rcp_cur_int'
    RCP_CUR_STR = 'rcp_cur_str',
    RCP_SET_LIST_RELATIVE = 'rcp_set_list_relative'
    RCP_SET_RELATIVE = 'rcp_set_relative'
    RCP_SUBSCRIBE = 'rcp_subscribe'
    RCP_CUR_CAM_INFO = 'rcp_cur_cam_info'

class RCP_KEYACTION:
    DISABLED = 0
    RECORD_START = 1
    RECORD_STOP = 2
    RECORD_TOGGLE = 3
    PLAYBACK_ENTER = 4
    PLAYBACK_EXIT = 5
    PLAYBACK_TOGGLE = 6
    PLAYBACK_PLAY = 7
    PLAYBACK_PAUSE = 8
    PLAYBACK_PLAY_PAUSE_TOGGLE = 9
    APERTURE_INCREMENT = 10
    APERTURE_DECREMENT = 11
    SHUTTER_INCREMENT = 12
    SHUTTER_DECREMENT = 13
    ISO_INCREMENT = 14
    ISO_DECREMENT = 15
    COLOR_TEMPERATURE_INCREMENT = 16
    COLOR_TEMPERATURE_DECREMENT = 17
    SDI_2_MAGNIFY_ON = 18
    SDI_2_MAGNIFY_OFF = 19
    SDI_1_MAGNIFY_ON = 20
    SDI_1_MAGNIFY_OFF = 21
    SDI_1_SDI_2_MAGNIFY_ON = 22
    SDI_1_SDI_2_MAGNIFY_OFF = 23
    FALSE_COLOR_CYCLE_NEXT = 24
    FALSE_COLOR_CYCLE_PREV = 25
    PEAKING_CYCLE_NEXT = 26
    PEAKING_CYCLE_PREV = 27
    TOOLS_CYCLE_NEXT = 28
    TOOLS_CYCLE_PREV = 29
    APPLY_PRESET = 30
    AUTO_WB = 31
    EJECT_MEDIA = 32
    FORMAT_MEDIA = 33
    JAM_TC_TO_TOD = 34
    START_AF = 35
    SAVE_LOG = 36
    SDI_1_MAGNIFY_TOGGLE = 37
    SDI_2_MAGNIFY_TOGGLE = 38
    PRE_RECORD_ENABLE_TOGGLE = 39
    PRE_RECORD_CANCEL = 40
    FALSE_COLOR_TOGGLE = 41
    PEAKING_TOGGLE = 42
    LOG_VIEW_TOGGLE = 43
    ZEBRA_1_TOGGLE = 44
    ZEBRA_2_TOGGLE = 45
    SDI_1_GUIDES_TOGGLE = 46
    SDI_2_GUIDES_TOGGLE = 47
    SDI_1_TOOLS_TOGGLE = 48
    SDI_2_TOOLS_TOGGLE = 49
    SDI_1_OVERLAY_TOGGLE = 50
    SDI_2_OVERLAY_TOGGLE = 51
    FRAME_GUIDE_1_TOGGLE = 52
    FRAME_GUIDE_2_TOGGLE = 53
    FRAME_GUIDE_3_TOGGLE = 54
    CENTER_GUIDE_TOGGLE = 55
    ND_INCREMENT = 56
    ND_DECREMENT = 57
    DSI_1_MAGNIFY_ON = 58
    DSI_1_MAGNIFY_OFF = 59
    DSI_1_MAGNIFY_TOGGLE = 60
    DSI_1_GUIDES_TOGGLE = 61
    DSI_1_TOOLS_TOGGLE = 62
    DSI_1_OVERLAY_TOGGLE = 63
    ND_CLEAR_TOGGLE = 64
    SENSOR_FLIP_TOGGLE = 65
    SYNC_SHIFT_INC_SMALL = 66
    SYNC_SHIFT_DEC_SMALL = 67
    SYNC_SHIFT_INC_MEDIUM = 68
    SYNC_SHIFT_DEC_MEDIUM = 69
    SYNC_SHIFT_INC_LARGE = 70
    SYNC_SHIFT_DEC_LARGE = 71
    AUX_1_TOGGLE = 72
    AUX_2_TOGGLE = 73
    AUX_3_TOGGLE = 74
    RS_TOGGLE_24V = 75
    EJECT_USBC_MEDIA = 76
    COUNT = 77

class RCPMessage:
    def __init__(self, data: dict) -> None:
        self.data = data

    def __getitem__(self, key):
        return self.data[key]

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
            "type": RCP_TYPE.RCP_GET_TYPES
        }


class RCPConfig(RCPMessage):

    def __init__(self) -> None:

        self.data = {
            "type": RCP_TYPE.RCP_CONFIG,
            "strings_decoded": 0,
            "json_minified": 1,
            "include_cacheable_flags": 0,
            "encoding_type": "legacy",
            "client": {"name": "My Awesome Control App", "version": "0.1", 'version_num': [0,1]},
        }

class RCPSubscribe(RCPMessage):

    def __init__(self, param_id: int, subscribe:bool = True) -> None:
        self.data  = {
            "type": RCP_TYPE.RCP_SUBSCRIBE,
            "id": param_id,
            "on_off": subscribe
        }

class RCPParam:

    def __init__(self, number:int, string:str) -> None:
        self.number = number
        self.string = string


class RCPParamList:

    def __init__(self, cur: int, param_list : List[RCPParam]) -> None:
        self.cur = cur 
        self.param_list = param_list 
        

class RCPSet(RCPMessage):

    def __init__(self, param_id:str, value=None, x=None, y=None, width=None, height=None, action:RCP_KEYACTION=None, held=None, argument=None ) -> None:
        self.data = {
            "type": RCP_TYPE.RCP_SET,
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
            self.data['action'] = action
        if argument:
            self.data['argument'] = argument

class RCPSetRelative(RCPMessage):

    def __init__(self, param_id:str, offset) -> None:
        self.data = {
            "type": RCP_TYPE.RCP_SET_RELATIVE,
            "id": param_id,
            "offset": offset
        }

class RCPSetListRelative(RCPMessage):
    """ Set a parameter offset from current list"""

    def __init__(self, param_id:str, offset:int) -> None:
        self.data = {
            "type": RCP_TYPE.RCP_SET_LIST_RELATIVE,
            "id": param_id,
            "offset": offset
        }

class RCPGetList(RCPMessage):

    def __init__(self, param_id: RCP_PARAM ) -> None:
        self.data = {
            "type":RCP_TYPE.RCP_GET_LIST,
            "id": param_id,
        }

class RCPGet(RCPMessage):

    def __init__(self, param_id:str) -> None:
        self.data = {
            "type": RCP_TYPE.RCP_GET,
            "id": param_id,
        }

get_fps = RCPGetList(RCP_PARAM.FPS)
get_iso = RCPGetList(RCP_PARAM.ISO)

iso_plus = RCPSetListRelative(RCP_PARAM.ISO, +1)
iso_minus = RCPSetListRelative(RCP_PARAM.ISO, -1)

fps_plus  = RCPSetListRelative(RCP_PARAM.FPS, +1)
fps_minus = RCPSetListRelative(RCP_PARAM.FPS, -1)

af_on = RCPSet(RCP_PARAM.AUTOFOCUS, 1)
af_off = RCPSet(RCP_PARAM.AUTOFOCUS, 0)