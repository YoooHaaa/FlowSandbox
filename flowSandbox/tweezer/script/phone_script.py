# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : phone_script.py
# Time       ：2020/10/20 16:16
# Author     ：Rodney Cheung
"""
import os
import sys
import traceback

from tweezer.core.runtime_event import RuntimeEvent, RuntimeEventType
from tweezer.config.config import Configor
from tweezer.core.plugin_loader import PluginLoader
from tweezer.core.top_app_monitor import TopAppMonitor
from tweezer.resource import constant
from tweezer.resource.resource import CwdResource
from tweezer.resource.runtime import Runtime
from tweezer.script.base_script import BaseScript
from tweezer.util.frida_switcher import FridaSwitcher
from tweezer.util.wrapper import exit_tweezer
from wisbec.android.adb import Adb
from wisbec.logging.log import Log
from wisbec.network.interface import Interface


class PhoneScript(BaseScript):
    def __init__(self):
        super().__init__()
        # choose listen ip and port
        Runtime().proxy_port = self.get_mitmproxy_port()
        Runtime().proxy_host = self.choose_proxy_inet()

        Log.info('已选取代理IP： {} {}', Runtime().proxy_host, Runtime().proxy_port)
        # 设置手机全局代理
        if not Adb.set_adb_proxy(Runtime().proxy_host, Runtime().proxy_port):
            os._exit(0)  # 用于线程中退出
        # start plugins
        try:
            PluginLoader(CwdResource.get_plugin_path()).start_all()
        except Exception as e:
            traceback.print_exc()
        # start app switch monitor

        self.__start_app_monitor()

    @staticmethod
    def get_mitmproxy_port() -> int:
        argc = len(sys.argv)
        for i in range(argc):
            v = sys.argv[i]
            if v == '-p' or v == '--listen-port':
                return int(sys.argv[i + 1])
        return 8080

    @staticmethod
    def choose_proxy_inet() -> str:
        interfaces = Interface.get_active_interfaces()
        if len(interfaces) == 0:
            Log.error('无法获取本机IP, 请确认已连接网络！')
            exit_tweezer()
        elif len(interfaces) == 1:
            Log.info('选择默认网络接口!')
            return interfaces[0].m_ip_addr.strip()
        else:
            msg = '请选择要使用的代理IP:{}'.format(os.linesep)
            i = 1
            ip_dict = {}
            for interface in interfaces:
                msg += '{0}\t{1}\t{2}{3}'.format(i, interface.m_iface_name, interface.m_ip_addr, os.linesep)
                ip_dict[i - 1] = interface.m_ip_addr
                i += 1
            Log.info(msg)
            while True:
                _id = int(input('请输入id：')) - 1
                if _id < 0 or _id >= len(interfaces):
                    Log.error('id输入错误')
                else:
                    break
            return ip_dict[_id]

    @staticmethod
    def __start_app_monitor():
        monitor = TopAppMonitor(Runtime().device_id, Configor.get_tweezer_conf()['no_proxy_apps'])
        monitor.add_no_proxy_apps(Adb.get_system_packages(Runtime().device_id))
        monitor.start_monitor(on_pkg_switch)
        Log.info('开始监控手机APP切换...')



def on_pkg_switch(top_pkg_name: str):
    Log.warning("手机APP被切换为 {}, 监控切换...", top_pkg_name)
    RuntimeEvent().on_event(RuntimeEventType.SWITCHED_APP, pkg=top_pkg_name)


addons = [
    PhoneScript()
]
