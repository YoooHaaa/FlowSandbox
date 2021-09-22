# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : url.py
# Time       ：10/28/20 11:45
# Author     ：Rodney Cheung
"""


class UrlInfo:
    def __init__(self, host='', port=8000, user=None, pwd=None):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__pwd = pwd

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        self.__user = value

    @property
    def pwd(self):
        return self.__pwd

    @pwd.setter
    def pwd(self, value):
        self.__pwd = value
