# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : apk_info.py
# Time       ：10/22/20 13:55
# Author     ：Rodney Cheung
"""


class ApkInfo:
    def __init__(self, pkg_name='', app_name='', version=''):
        self.__pkg_name = pkg_name
        self.__app_name = app_name
        self.__version = version

    @property
    def pkg_name(self):
        return self.__pkg_name

    @pkg_name.setter
    def pkg_name(self, value):
        self.__pkg_name = value

    @property
    def app_name(self):
        return self.__app_name

    @app_name.setter
    def app_name(self, value):
        self.__app_name = value

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value

    def __getstate__(self):
        state = {
            '包名': self.__pkg_name,
            '应用名': self.__app_name,
            '版本号': self.__version
        }
        return state

    def __eq__(self, other):
        if isinstance(other, ApkInfo):
            return self.__version == other.__version and \
                   self.__pkg_name == other.__pkg_name and \
                   self.__app_name == other.__app_name
        return False
