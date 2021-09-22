# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : config.py
# Time       ：2020/8/31 10:00
# Author     ：Rodney Cheung
"""

import json

from tweezer.model.ad_sdk import AdSdkType
from tweezer.resource.resource import CwdResource
from wisbec.filesystem.filesystem import FilesystemUtil


class Configor:
    m_known_ad_platforms_conf = None
    m_tweezer_conf = None
    m_ad_filter_rules_conf = None
    m_packet_filter_rules_conf = None
    m_url_filter_rules_conf = None
    m_tuia_ad_cap_rules_conf = None
    m_weli_ad_cap_rules_conf = None

    @classmethod
    def __load_config(cls, conf_path):
        if not FilesystemUtil.is_file_exist(conf_path):
            return None
        with open(conf_path, 'rb') as f:
            return json.load(f)

    @classmethod
    def load_config(cls):
        cls.m_known_ad_platforms_conf = cls.__load_config(CwdResource.get_known_ad_platforms_conf_path())
        cls.m_tweezer_conf = cls.__load_config(CwdResource.get_tweezer_conf_path())
        cls.m_ad_filter_rules_conf = cls.__load_config(CwdResource.get_ad_filter_rules_conf_path())
        cls.m_url_filter_rules_conf = cls.__load_config(CwdResource.get_url_filter_rules_conf_path())
        cls.m_packet_filter_rules_conf = cls.__load_config(CwdResource.get_packet_filter_rules_conf_path())
        cls.m_tuia_ad_cap_rules_conf = cls.__load_config(CwdResource.get_tuia_ad_cap_rules_conf_path())
        cls.m_weli_ad_cap_rules_conf = cls.__load_config(CwdResource.get_weli_ad_cap_rules_conf_path())

    @classmethod
    def get_known_ad_platforms_conf(cls):
        return cls.m_known_ad_platforms_conf

    @classmethod
    def get_tweezer_conf(cls):
        return cls.m_tweezer_conf

    @classmethod
    def get_ad_filter_rules_conf(cls):
        return cls.m_ad_filter_rules_conf

    @classmethod
    def get_packet_filter_conf(cls) -> dict:
        return cls.m_tweezer_conf['plugins']['general']['packet_filter']['config']

    @classmethod
    def get_url_filter_conf(cls) -> dict:
        return cls.m_tweezer_conf['plugins']['general']['url_filter']['config']

    @classmethod
    def get_hotkey_screen_cap_conf(cls) -> dict:
        return cls.m_tweezer_conf['plugins']['hotkey']['hotkey_screen_cap']['config']

    @classmethod
    def get_hotkey_exit_conf(cls) -> dict:
        return cls.m_tweezer_conf['plugins']['hotkey']['hotkey_screen_cap']['config']


    @classmethod
    def get_hotkey_packet_cap_conf(cls) -> dict:
        return cls.m_tweezer_conf['plugins']['hotkey']['hotkey_exit']['config']

    @classmethod
    def get_hotkey_switch_net_traffic_conf(cls) -> dict:
        return cls.m_tweezer_conf['plugins']['hotkey']['hotkey_switch_net_traffic']['config']

    @classmethod
    def get_hotkey_switch_location_conf(cls) -> dict:
        return cls.m_tweezer_conf['plugins']['hotkey']['hotkey_switch_location']['config']

    @classmethod
    def get_ad_cap_conf(cls, ad_sdk_type: AdSdkType) -> dict:
        return cls.m_tweezer_conf['plugins']['ad'][ad_sdk_type.name + '_ad_cap']['config']

    @classmethod
    def get_packet_filter_rules_conf(cls):
        return cls.m_packet_filter_rules_conf

    @classmethod
    def get_url_filter_rules_conf(cls):
        return cls.m_url_filter_rules_conf

    @classmethod
    def get_tuia_ad_cap_rules_conf(cls):
        return cls.m_tuia_ad_cap_rules_conf

    @classmethod
    def get_weli_ad_cap_rules_conf(cls):
        return cls.m_weli_ad_cap_rules_conf

    @classmethod
    def get_loopback_upstream_port(cls):
        return 34567
