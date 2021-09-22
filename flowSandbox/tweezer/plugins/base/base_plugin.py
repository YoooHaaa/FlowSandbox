# coding=utf-8

import abc
import os
import threading

from tweezer.model.apk_info import ApkInfo
from tweezer.resource.runtime import Runtime
from wisbec.android.adb import Adb
from wisbec.logging.log import Log


class BasePlugin(metaclass=abc.ABCMeta):
    def __init__(self, apk_info=None):
        self.m_top_app: str = ''
        self.m_err_file_lock = threading.Lock()
        self.m_apk_info: ApkInfo = apk_info

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def register_event(self):
        pass

    def flush_app_info(self):
        try:
            app_name = Adb.get_app_name(Runtime().device_id, self.m_top_app)
            app_version = Adb.get_app_version(Runtime().device_id, self.m_top_app)
            self.m_apk_info = ApkInfo(self.m_top_app, app_name, app_version)
        except Exception as err:
            Log.error(str(err))

    def persist_err_content(self, err: str, save_path: str):
        with self.m_err_file_lock, open(save_path, 'a+') as f:
            f.write(err)
            f.write(os.linesep)
