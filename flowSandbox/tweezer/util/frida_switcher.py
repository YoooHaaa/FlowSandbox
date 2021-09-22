# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : frida_switcher.py
# Time       ：12/9/20 15:54
# Author     ：Rodney Cheung
"""
import os

from tweezer.core.faker.network_faker import NetworkFaker
from tweezer.core.frida_hooker import FridaHooker
from tweezer.core.http_proxy import HttpProxy
from tweezer.core.mitm_cert import MitmCert
from tweezer.core.runtime_event import RuntimeEvent, RuntimeEventType
from tweezer.model.traffic_type import TrafficType
from tweezer.resource import constant
from tweezer.resource.runtime import Runtime
from tweezer.util.TerminateTweezer import TweezerTerminator
from wisbec import path
from wisbec.design_patterns.singleton import SingletonType
from wisbec.logging.log import Log


class FridaSwitcher(metaclass=SingletonType):
    def __init__(self):
        pass
        # self.m_hooker: FridaHooker = FridaHooker.instance(Runtime().device_id)
        # self.m_http_proxy: HttpProxy = HttpProxy.instance(Runtime().device_id)
        # self.m_network_faker: NetworkFaker = NetworkFaker.instance(Runtime().device_id)

    # def install_mitm_cert(self, pkg_name: str) -> bool:
    #     try:
    #         cacert_path = os.path.join(path.home_dir(), '.mitmproxy', constant.CACERTS_NAME)
    #         cert_installer = MitmCert(Runtime().device_id, cacert_path)
    #         Log.info('安装CA证书...')
    #         cert_installer.install(pkg_name)
    #         Log.info('CA证书安装成功！')
    #
    #         mitm_cert = cert_installer.get_frida_script(pkg_name)
    #         if self.m_hooker.spawn_hook(list_scripts_code=[mitm_cert],
    #                                     trace_new_processes=True) == -1:
    #             return False
    #         return True
    #     except Exception as e:
    #         Log.error('证书安装失败, 原因:{}', str(e))
    #         return False
    #
    # def on_frida_switch(self, top_pkg_name: str):
    #     Log.warning("手机APP被切换为 {}, 监控切换中, 请稍等...", top_pkg_name)
    #     RuntimeEvent().on_event(RuntimeEventType.SWITCHED_APP, pkg=top_pkg_name)
    #     self.m_hooker.unhook_all()
    #     if not self.m_hooker.spawn_begin(top_pkg_name):
    #         Log.error("frida begin failed")
    #         return
    #     if not self.install_mitm_cert(top_pkg_name):
    #         TweezerTerminator.instance().terminate()
    #     if self.m_hooker.spawn_hook([self.m_http_proxy.get_frida_script()], None, True) == -1:
    #         Log.error("frida hook package failed")
    #         return
    #     # true only as hotkey_switch_net_traffic.py has been loaded
    #     if Runtime().traffic_faker_on:
    #         if Runtime().exec_env.traffic_type == TrafficType.WIFI:
    #             self.m_network_faker.fake_as_wifi(Runtime().fake_wifi_info)
    #         else:
    #             self.m_network_faker.fake_as_mobile()
    #     if not self.m_hooker.spawn_finish():
    #         Log.error("frida finish failed")
    #         return
    #     self.m_http_proxy.start_proxy(top_pkg_name, Runtime().proxy_host, Runtime().proxy_port)
    #     Log.warning("监控切换成功, 正在监控{}", top_pkg_name)
