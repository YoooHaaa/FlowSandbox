# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : area.py
# Time       ：10/27/20 17:58
# Author     ：Rodney Cheung
"""


class AreaInfo:
    def __init__(self, province='', city='', longitude=0, latitude=0):
        self.__province: str = province
        self.__city: str = city
        self.__longitude: float = longitude
        self.__latitude: float = latitude

    @property
    def province(self):
        return self.__province

    @province.setter
    def province(self, value):
        self.__province = value

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, value):
        self.__city = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        self.__longitude = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        self.__latitude = value
