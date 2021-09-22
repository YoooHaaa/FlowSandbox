# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : ad_plugin_output.py
# Time       ：10/22/20 14:06
# Author     ：Rodney Cheung
"""
from typing import List, Dict

from tweezer.model.ad_info import AdInfo
from tweezer.model.apk_info import ApkInfo
from tweezer.model.exec_env import ExecEnv
from tweezer.model.ad_sdk import AdSdkInfo


class AdPluginOutput:
    def __init__(self):
        self.__ad_info_map: Dict[str, AdInfo] = dict()
        self.__apk_info = None
        self.__sdk_info = None
        self.__exec_env = None

    @property
    def ad_info_map(self):
        return self.__ad_info_map

    @ad_info_map.setter
    def ad_info_map(self, value):
        self.__ad_info_map = value

    @property
    def apk_info(self):
        return self.__apk_info

    @apk_info.setter
    def apk_info(self, value):
        self.__apk_info = value

    @property
    def sdk_info(self):
        return self.__sdk_info

    @sdk_info.setter
    def sdk_info(self, value):
        self.__sdk_info = value

    @property
    def exec_env(self):
        return self.__exec_env

    @exec_env.setter
    def exec_env(self, value):
        self.__exec_env = value

    def __getstate__(self):
        state = {
            '执行环境信息': self.__exec_env,
            'SDK信息': self.__sdk_info,
            'APK信息': self.__apk_info,
            '广告信息': list(self.__ad_info_map.values())
        }
        return state
