# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : ad_fetch_err_info.py
# Time       ：11/25/20 11:24
# Author     ：Rodney Cheung
"""


class AdFetchErrInfo:
    def __init__(self, err_msg='', err_code=0):
        self.__err_msg: str = err_msg
        self.__err_code: int = err_code

    @property
    def err_msg(self):
        return self.__err_msg

    @err_msg.setter
    def err_msg(self, value):
        self.__err_msg = value

    @property
    def err_code(self):
        return self.__err_code

    @err_code.setter
    def err_code(self, value):
        self.__err_code = value
