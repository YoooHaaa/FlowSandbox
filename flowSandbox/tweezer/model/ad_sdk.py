# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : ad_sdk.py
# Time       ：10/22/20 14:59
# Author     ：Rodney Cheung
"""
from enum import Enum


class AdSdkType(Enum):
    kuaishou = 0
    gdt = 1
    tuia = 2
    toutiao = 3
    qutoutiao = 4
    weli = 5
    baidu = 6

    @classmethod
    def chinese_name_dict(cls) -> dict:
        d = {
            cls.kuaishou: '快手',
            cls.gdt: '广点通',
            cls.tuia: '推啊',
            cls.toutiao: '穿山甲',
            cls.qutoutiao: '趣头条',
            cls.weli: '微鲤',
            cls.baidu: '百青藤'
        }
        return d

    def chinese_name(self) -> str:
        return self.chinese_name_dict()[self]


class AdSdkInfo:
    def __init__(self, name='', version=''):
        self.__name: str = name
        self.__version: str = version

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        self.__version = value

    def __getstate__(self):
        state = {
            '广告SDK名称': self.__name,
            '广告SDK版本': self.__version
        }
        return state

    def __eq__(self, other):
        if isinstance(other, AdSdkInfo):
            return self.__name == other.__name and \
                   self.__version == other.__version
        return False
