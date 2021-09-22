# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : constant.py
# Time       ：2020/8/20 16:24
# Author     ：Rodney Cheung
"""
from tweezer.util.wrapper import now

TIME_DIR_NAME = now()

BELOW_FLOW_COUNT = 50  # 持续抓取下文包的个数
BELOW_FLOW_MIN_INTERVAL = 10  # 持续抓取下文包的最大间隔 s
SU_PATHS = ['/system/bin/su',
            '/system/xbin/su',
            '/sbin/su',
            '/system/su',
            '/system/bin/.ext/.su']
CACERTS_ADDED_DIR = '/system/etc/security/cacerts'
CACERTS_NAME = 'mitmproxy-ca-cert.pem'
CACERTS_HASH_NAME = 'c8750f0d.0'

SCREENSHOT_OUTPUT_DIR = 'HotkeyScreenCap'
MANUAL_SCREENSHOT_OUTPUT_DIR = 'HotkeyPacketCap'
PACKET_FILTER_OUTPUT_DIR = 'PacketFilter'
URL_FILTER_OUTPUT_DIR = 'UrlFilter'
AD_FILTER_OUTPUT_DIR = 'AdFilter'
GDT_AD_OUTPUT_DIR = 'GdtAd'
TUIA_AD_OUTPUT_DIR = 'TuiaAd'
TOUTIAO_AD_OUTPUT_DIR = 'ToutiaoAd'
WELI_AD_OUTPUT_DIR = 'WeliAd'

PACKET_FILTER_RULES_FILE = 'packet_filter_rules.json'
URL_FILTER_RULES_FILE = 'url_filter_rules.json'
AD_FILTER_RULES_FILE = 'ad_filter_rules.json'
TUIA_AD_RULES_FILE = 'tuia_ad_cap_rules.json'
WELI_AD_RULES_FILE = 'weli_ad_cap_rules.json'

APP_DATA_PATH_TEMP_TP = '/data/data/{}/tweezer-{}'