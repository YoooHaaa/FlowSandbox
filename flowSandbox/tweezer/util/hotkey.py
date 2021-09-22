# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : hotkey.py
# Time       ：2020/9/4 09:24
# Author     ：Rodney Cheung
"""

from typing import Set, AnyStr

from wisbec import system


def get_invalid_hotkey() -> Set[AnyStr]:
    if system.is_mac_os():
        return {'option', 'shift', 'ctrl'}
    else:
        return set()
