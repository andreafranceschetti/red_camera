import json 

class RCP_PARAM:
    FPS = "RCP_PARAM_SENSOR_FRAME_RATE"
    ISO = "RCP_PARAM_ISO"
    AUTOFOCUS = "RCP_PARAM_AF_ENABLE"
    COLOR_TEMP = "RCP_PARAM_COLOR_TEMPERATURE"
    APERTURE = "RCP_PARAM_APERTURE"
    AUDIO_EXTERNAL_LEFT_GAIN = 'RCP_PARAM_AUDIO_EXTERNAL_LEFT_GAIN'
    FAN_MODE = 'RCP_PARAM_FAN_MODE'
    CAMERA_INFO = 'RCP_PARAM_CAMERA_INFO'

class RCP_TYPE:
    RCP_GET = 'rcp_get'
    RCP_GET_TYPES = 'rcp_get_types'
    RCP_CUR_TYPES = 'rcp_cur_types'
    RCP_GET_LIST = 'rcp_get_list'
    RCP_CONFIG = 'rcp_config'
    RCP_SET = 'rcp_set'
    RCP_SET_LIST_RELATIVE = 'rcp_set_list_relative'
    RCP_SET_RELATIVE = 'rcp_set_relative'
    RCP_SUBSCRIBE = 'rcp_subscribe'
    RCP_CUR_CAM_INFO = 'rcp_cur_cam_info'


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

class RCPSet(RCPMessage):

    def __init__(self, param_id:str, value=None, x=None, y=None, width=None, height=None, action=None, held=None, argument=None ) -> None:
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
            self.data['action'] =action
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

    def __init__(self, param_id:str, offset:int) -> None:
        self.data = {
            "type": RCP_TYPE.RCP_SET_LIST_RELATIVE,
            "id": param_id,
            "offset": offset
        }

class RCPGetList(RCPMessage):

    def __init__(self, param_id:str) -> None:
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