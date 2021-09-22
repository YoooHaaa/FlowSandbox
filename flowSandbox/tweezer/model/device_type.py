# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : device_type.py
# Time       ：11/4/20 15:35
# Author     ：Rodney Cheung
"""
from enum import Enum


class DeviceType(Enum):
    RealDevice = 0
    Emulator = 1
