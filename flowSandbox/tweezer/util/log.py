# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : log.py
# Time       ：11/11/20 17:36
# Author     ：Rodney Cheung
"""
from wisbec.logging.log import Log


class LogUtil:
    @classmethod
    def critical_exception(cls, exception: Exception):
        if isinstance(exception, UnicodeDecodeError):
            Log.critical('decode err')
            return
        elif isinstance(exception, KeyError):
            Log.critical('key err')
        elif isinstance(exception, ValueError):
            Log.critical('value err')
        else:
            Log.critical(str(exception))
