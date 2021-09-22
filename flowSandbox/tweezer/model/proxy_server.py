# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : proxy_server.py
# Time       ：10/27/20 18:05
# Author     ：Rodney Cheung
"""

from tweezer.model.area import AreaInfo
from tweezer.model.url import UrlInfo


class ProxyServerInfo:
    def __init__(self, area_info=None, url_info=None):
        self.__area_info: AreaInfo = area_info
        self.__url_info: UrlInfo = url_info

    @property
    def area_info(self):
        return self.__area_info

    @area_info.setter
    def area_info(self, value):
        self.__area_info = value

    @property
    def url_info(self):
        return self.__url_info

    @url_info.setter
    def url_info(self, value):
        self.__url_info = value
