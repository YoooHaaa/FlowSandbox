# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : params.py
# Time       ：11/4/20 12:01
# Author     ：Rodney Cheung
"""


class Params:
    def __init__(self, proxy_port='8000', version=False, flow=''):
        self.__proxy_port: str = proxy_port
        self.__version: bool = version
        self.__flow: str = flow

    @property
    def proxy_port(self):
        return self.__proxy_port

    @proxy_port.setter
    def proxy_port(self, value):
        self.__proxy_port = value

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value

    @property
    def flow(self):
        return self.__flow

    @flow.setter
    def flow(self, value):
        self.__flow = value