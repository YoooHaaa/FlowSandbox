# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : resource.py
# Time       ：2020/8/20 15:26
# Author     ：Rodney Cheung
"""

import os
import shutil
from os.path import *

from wisbec import system
from wisbec.filesystem.filesystem import FilesystemUtil

from tweezer.resource import constant


class PackageResource:
    @classmethod
    def get_installation_pkg_path(cls) -> str:
        return join(dirname(abspath(__file__)), 'installation_pkg')

    @classmethod
    def get_mitmproxy_wheel_pkg_path(cls) -> str:
        return join(cls.get_installation_pkg_path(), 'mitmproxy-5.2-py3-none-any.whl')

    @classmethod
    def get_plugin_path(cls) -> str:
        return join(dirname(abspath(__file__)), '../plugins')

    @classmethod
    def get_config_path(cls) -> str:
        return join(dirname(abspath(__file__)), 'config')

    @classmethod
    def get_rules_path(cls) -> str:
        return join(dirname(abspath(__file__)), 'rules')

    @classmethod
    def get_persist_path(cls) -> str:
        return join(dirname(abspath(__file__)), 'persist')

    @classmethod
    def get_decrypt_jar_path(cls):
        return join(dirname(abspath(__file__)), 'decrypt', 'decryptor.jar')

    @classmethod
    def get_known_ad_platforms_conf_path(cls):
        return join(cls.get_config_path(), 'known_ad_platforms.json')

    @classmethod
    def get_tweezer_conf_path(cls):
        return join(cls.get_config_path(), 'tweezer_conf.json')

    @classmethod
    def get_adb_tool_path(cls):
        if system.is_linux():
            return join(cls.get_installation_pkg_path(), 'platform-tools_r30.0.4-linux.zip')
        elif system.is_mac_os():
            return join(cls.get_installation_pkg_path(), 'platform-tools_r30.0.4-darwin.zip')
        else:
            return join(cls.get_installation_pkg_path(), 'platform-tools_r30.0.4-windows.zip')

    @classmethod
    def get_frida_server_arm_path(cls):
        return join(cls.get_installation_pkg_path(), 'frida-server-14.1.2-android-arm')

    @classmethod
    def get_frida_server_arm64_path(cls):
        return join(cls.get_installation_pkg_path(), 'frida-server-14.1.2-android-arm64')

    @classmethod
    def get_mock_location_apk_path(cls):
        return join(cls.get_installation_pkg_path(), 'mock_location.apk')

    @classmethod
    def get_frida_base_path(cls):
        return join(cls.get_persist_path(), 'frida_base.js')

    @classmethod
    def get_frida_core_path(cls):
        return join(cls.get_persist_path(), 'frida_core')

    @classmethod
    def get_frida_http_proxy_path(cls):
        return join(cls.get_frida_core_path(), 'http_proxy.js')

    @classmethod
    def get_frida_mitm_cert_path(cls):
        return join(cls.get_frida_core_path(), 'mitm_cert.js')

    @classmethod
    def get_geoinfo_china_path(cls):
        return join(cls.get_persist_path(), 'geoinfo-china.json')


class CwdResource:

    @classmethod
    def get_tweezer_path(cls) -> str:
        return join(os.getcwd(), 'tweezer_usr')

    @classmethod
    def get_log_path(cls) -> str:
        return join(cls.get_tweezer_path(), 'log')

    @classmethod
    def get_output_path(cls) -> str:
        return join(cls.get_tweezer_path(), 'output', constant.TIME_DIR_NAME)

    @classmethod
    def get_rules_path(cls):
        return join(cls.get_tweezer_path(), 'rules')

    @classmethod
    def get_config_path(cls) -> str:
        return join(cls.get_tweezer_path(), 'config')

    @classmethod
    def get_plugin_path(cls) -> str:
        return join(cls.get_tweezer_path(), 'plugin')

    @classmethod
    def get_plugin_output_path(cls) -> str:
        return join(cls.get_output_path(), 'plugin_output')

    @classmethod
    def get_known_ad_platforms_conf_path(cls):
        return join(cls.get_config_path(), 'known_ad_platforms.json')

    @classmethod
    def get_tweezer_conf_path(cls):
        return join(cls.get_config_path(), 'tweezer_conf.json')

    @classmethod
    def get_fake_proxy_server_conf_path(cls):
        return join(cls.get_config_path(), 'default_fake_proxy_server.json')

    @classmethod
    def get_fake_net_traffic_conf_path(cls):
        return join(cls.get_config_path(), 'default_fake_net_traffic.ini')

    @classmethod
    def get_ad_filter_rules_conf_path(cls):
        return join(cls.get_rules_path(), constant.AD_FILTER_RULES_FILE)

    @classmethod
    def get_url_filter_rules_conf_path(cls):
        return join(cls.get_rules_path(), constant.URL_FILTER_RULES_FILE)

    @classmethod
    def get_packet_filter_rules_conf_path(cls):
        return join(cls.get_rules_path(), constant.PACKET_FILTER_RULES_FILE)

    @classmethod
    def get_tuia_ad_cap_rules_conf_path(cls):
        return join(cls.get_rules_path(), constant.TUIA_AD_RULES_FILE)

    @classmethod
    def get_weli_ad_cap_rules_conf_path(cls):
        return join(cls.get_rules_path(), constant.WELI_AD_RULES_FILE)


def copy_resources_to_cwd():
    if not FilesystemUtil.is_directory_exist(CwdResource.get_rules_path()):
        shutil.copytree(PackageResource.get_rules_path(), CwdResource.get_rules_path())
    if not FilesystemUtil.is_directory_exist(CwdResource.get_config_path()):
        shutil.copytree(PackageResource.get_config_path(), CwdResource.get_config_path())
    if not FilesystemUtil.is_directory_exist(CwdResource.get_plugin_path()):
        shutil.copytree(PackageResource.get_plugin_path(), CwdResource.get_plugin_path())


def remove_resources_from_cwd():
    if FilesystemUtil.is_directory_exist(CwdResource.get_tweezer_path()):
        FilesystemUtil.remove(CwdResource.get_tweezer_path())
