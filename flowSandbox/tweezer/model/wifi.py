# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : wifi.py
# Time       ：10/27/20 15:37
# Author     ：Rodney Cheung
"""


class WifiInfo:
    def __init__(self, ip='', ssid='', bssid='', mac=''):
        self.m_ip: str = ip
        self.m_ssid: str = ssid
        self.m_bssid: str = bssid
        self.m_mac: str = mac
