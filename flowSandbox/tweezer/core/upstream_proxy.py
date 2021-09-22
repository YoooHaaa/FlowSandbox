# coding=utf-8

import socket
import threading
import time
import traceback

from colorlog import logging

from tweezer.config.config import Configor
from tweezer.util import http_proxy
from tweezer.util.log import LogUtil
from wisbec.logging.log import Log


class UpstreamProxy:
    s_instance = None
    m_is_loopback_proxy_on = False
    s_upstream_proxy = ('127.0.0.1', Configor.get_loopback_upstream_port(), None, None)


    def __init__(self):
        caller = traceback.extract_stack()[-2][2]
        assert caller == 'instance', "Please use {}.get_instance() got it.".format(UpstreamProxy.__name__)
        pass


    @classmethod
    def instance(cls):
        # 每个adb 1个单例
        if cls.s_instance is None:
            cls.s_instance = cls()
        return cls.s_instance


    @staticmethod
    def __is_tcp_port_open(port):
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.bind(('0.0.0.0', port))
            tcp_client.close()
            return False
        except Exception as e:
            return True


    def __thread_loopback_proxy(self):
        try:
            arguments = ['--enable-web-server', '--port', str(Configor.get_loopback_upstream_port()),
                         '--hostname', '127.0.0.1', '--num-workers', '100']
            http_proxy.proxy_entry(input_args=arguments)
        except Exception as e:
            LogUtil.critical_exception(e)
        self.m_is_loopback_proxy_on = False


    def start_loopback_proxy(self):
        tweezer_handler = None
        if len(logging.getLogger().handlers) > 0:
            tweezer_handler = logging.getLogger().handlers[0]

        if not self.m_is_loopback_proxy_on:
            self.m_is_loopback_proxy_on = True
            threading.Thread(target=self.__thread_loopback_proxy).start()
            time.sleep(1)

            # 清除 proxy.py模块对logging的handler的更改，否则会与tweezer的配置冲突，导致1条日志输出3次
            for h in logging.getLogger().handlers:
                if h != tweezer_handler:
                    logging.getLogger().removeHandler(h)
            return self.m_is_loopback_proxy_on
        return True

    def get_upstream_proxy(self):
        return self.s_upstream_proxy

    def __set_upstream_proxy(self, host, port, user=None, pwd=None):
        self.s_upstream_proxy = (host, port, user, pwd)

    def stop(self):
        if self.start_loopback_proxy() is False:
            return False
        self.__set_upstream_proxy('127.0.0.1', Configor.get_loopback_upstream_port())
        return True

    # http server
    def start(self, host, port, user=None, pwd=None):
        self.__set_upstream_proxy(host, port, user, pwd)
