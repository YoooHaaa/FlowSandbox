# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : exec_env.py
# Time       ：10/22/20 13:48
# Author     ：Rodney Cheung
"""

from tweezer.model.traffic_type import TrafficType


class ExecEnv:
    def __init__(self, device_model='', sdk_level=27, traffic_type=TrafficType.WIFI, ip='127.0.0.1', gps=''):
        self.__device_model: str = device_model
        self.__sdk_level: int = sdk_level
        self.__traffic_type: TrafficType = traffic_type
        self.__ip: str = ip
        self.__gps = gps

    def __getstate__(self):
        state = {
            '设备型号': self.__device_model,
            'SDK号': self.__sdk_level,
            '流量类型': self.__traffic_type.name,
            'IP': self.__ip,
            'GPS': self.__gps
        }
        return state

    def __eq__(self, other):
        if isinstance(other, ExecEnv):
            return self.__ip == other.__ip and \
                   self.__gps == other.__gps and \
                   self.__sdk_level == other.__sdk_level and \
                   self.__device_model == other.__device_model and \
                   self.__traffic_type == other.__traffic_type
        return False

    @property
    def sdk_level(self):
        return self.__sdk_level

    @sdk_level.setter
    def sdk_level(self, value):
        self.__sdk_level = value

    @property
    def device_model(self):
        return self.__device_model

    @device_model.setter
    def device_model(self, value):
        self.__device_model = value

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        self.__ip = value

    @property
    def gps(self):
        return self.__gps

    @gps.setter
    def gps(self, value):
        self.__gps = value

    @property
    def traffic_type(self):
        return self.__traffic_type

    @traffic_type.setter
    def traffic_type(self, value):
        self.__traffic_type = value
