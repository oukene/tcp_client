import logging
import os
from .const import *
import yaml
import traceback


_LOGGER = logging.getLogger(__name__)

class SettingManager(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, name=None):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self._name = name
            self._settings = None
            # self.load_setting()

            cls._init = True

    def load_setting(self):
        # 셋팅을 로드
        filepath = DOMAIN + "/" + self._name + ".yaml"
        _LOGGER.debug("file path : " + str(filepath))
        if os.path.isdir(DOMAIN) == False:
            os.makedirs(DOMAIN)
        if os.path.isfile(filepath) == False:
            with open(filepath, "w") as f:
                f.write("host:\n\n")
                f.write("port:\n\n")
                f.write("sensor:\n\n")
                f.write("binary_sensor:\n\n")
                f.write("switch:\n\n")
                f.write("button:\n\n")
                pass
        
        with open(filepath) as f:
            self._settings = yaml.load(f, Loader=yaml.FullLoader)
            _LOGGER.debug("full settings error : " + str(self._settings))
    
    @staticmethod
    def get_settings():
        try:
            mgr = SettingManager()
            return mgr._settings
        except Exception as e:
            _LOGGER.debug("get setting error : " + traceback.format_exc())
            return None
