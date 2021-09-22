# coding=utf-8
from tweezer.model.exec_env import ExecEnv
from tweezer.model.wifi import WifiInfo
from wisbec.design_patterns.singleton import SingletonType


class Runtime(metaclass=SingletonType):
    def __init__(self):
        self.__device_id: str = ''
        self.__exec_env: ExecEnv = ExecEnv()
        self.__traffic_faker_on: bool = False
        self.__fake_wifi_info: WifiInfo = WifiInfo()
        self.__proxy_host: str = ''
        self.__proxy_port: int = 0

    @property
    def device_id(self):
        return self.__device_id

    @device_id.setter
    def device_id(self, value):
        self.__device_id = value

    @property
    def exec_env(self):
        return self.__exec_env

    @exec_env.setter
    def exec_env(self, value):
        self.__exec_env = value

    @property
    def traffic_faker_on(self):
        return self.__traffic_faker_on

    @traffic_faker_on.setter
    def traffic_faker_on(self, value):
        self.__traffic_faker_on = value

    @property
    def fake_wifi_info(self):
        return self.__fake_wifi_info

    @fake_wifi_info.setter
    def fake_wifi_info(self, value):
        self.__fake_wifi_info = value

    @property
    def proxy_host(self):
        return self.__proxy_host

    @proxy_host.setter
    def proxy_host(self, value):
        self.__proxy_host = value

    @property
    def proxy_port(self):
        return self.__proxy_port

    @proxy_port.setter
    def proxy_port(self, value):
        self.__proxy_port = value
