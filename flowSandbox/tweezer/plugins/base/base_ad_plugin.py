# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : base_ad_plugin.py
# Time       ：10/22/20 16:07
# Author     ：Rodney Cheung
"""
import abc
import os
import threading

from tweezer.core.output import Output
from tweezer.core.screen_cap import ScreenCap
from tweezer.model.ad_info import AdInfo
from tweezer.model.ad_sdk import AdSdkInfo
from tweezer.model.exec_env import ExecEnv
from tweezer.plugins.base.base_plugin import BasePlugin
from tweezer.resource.resource import CwdResource
from tweezer.resource.runtime import Runtime
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log


class BaseAdPlugin(BasePlugin, metaclass=abc.ABCMeta):
    def __init__(self, sdk_info=None, exec_env=None):
        super().__init__()
        # variable
        self.m_sdk_info: AdSdkInfo = sdk_info
        self.m_exec_env: ExecEnv = exec_env
        self.m_screen_cap_delay_time: int = 0
        # func
        self.get_sdk_info()
        self.load_conf()

    @abc.abstractmethod
    def get_sdk_info(self):
        """
        set sdk info
        :return:
        """
        pass

    @abc.abstractmethod
    def load_conf(self):
        """
        load plugin config in tweezer_conf.json
        :return:
        """
        pass

    def persist_ad_info(self, ad_info: AdInfo):
        if ad_info is not None:
            Output().persist(ad_info, self.m_apk_info, self.m_sdk_info,
                             os.path.join(self.get_output_path(), 'output.json'))
        else:
            Log.error('empty ad info')

    def get_output_path(self) -> str:
        output_dir = os.path.join(CwdResource.get_output_path(), self.m_apk_info.app_name, self.m_sdk_info.name)
        FilesystemUtil.create_directories(output_dir)
        return output_dir

    def get_err_save_path(self, file_name: str) -> str:
        return os.path.join(self.get_output_path(), file_name)

    @staticmethod
    def self_increasing_screen_cap_name(file_name: str) -> str:
        base_name, ext = os.path.splitext(file_name)
        components = base_name.split('_')
        series = int(components[-1]) + 1
        new_file_name = ''
        for i in range(len(components) - 1):
            if i != 0:
                new_file_name += '_'
            new_file_name += components[i]
        return new_file_name + '_' + str(series) + ext

    def get_self_increasing_screenshot_path(self, p: str):
        while FilesystemUtil.is_file_exist(p):
            Log.info('截图已经存在:{}', p)
            p = self.self_increasing_screen_cap_name(p)
            Log.info('新截图名称:{}', p)
        return p

    def thread_screen_cap(self, screenshot_path='', overwrite=False):
        """
        Capture screen on another thread.
        if overwrite is True,screen_path must be
        'xx_{$NUM}.png' format.{$NUM} can be any integers.
        For instance,if screenshot_path is screen_0.png and
        screen_0.png already exists.screen_1.png will be
        created.
        :param screenshot_path: screenshot save path
        :param overwrite: overwrite if screenshot_path is
        already exist
        :return:
        """
        if not overwrite:
            p = self.get_self_increasing_screenshot_path(screenshot_path)
        else:
            p = screenshot_path
        threading.Thread(target=ScreenCap.delay_capture,
                         args=(Runtime().device_id,
                               p,
                               self.m_screen_cap_delay_time)).start()
