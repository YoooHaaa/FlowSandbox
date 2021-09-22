# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : output.py
# Time       ：10/22/20 14:21
# Author     ：Rodney Cheung
"""
import threading
from queue import Queue
from typing import Dict

import jsonpickle

from tweezer.model.ad_info import AdInfo
from tweezer.model.ad_plugin_output import AdPluginOutput
from tweezer.model.apk_info import ApkInfo
from tweezer.model.exec_env import ExecEnv
from tweezer.model.ad_sdk import AdSdkInfo
from tweezer.resource.runtime import Runtime
from wisbec.design_patterns.singleton import SingletonType
from wisbec.logging.log import Log


class OutputHistoryKey:
    def __init__(self, sdk_info: AdSdkInfo, apk_info: ApkInfo, exec_env: ExecEnv):
        self.m_sdk_info = sdk_info
        self.m_apk_info = apk_info
        self.m_exec_env = exec_env

    def __hash__(self):
        return hash(
            self.m_apk_info.pkg_name +
            self.m_sdk_info.name +
            self.m_exec_env.ip +
            self.m_exec_env.gps +
            str(self.m_exec_env.traffic_type))

    def __eq__(self, other):
        if isinstance(other, OutputHistoryKey):
            return self.m_apk_info == other.m_apk_info \
                   and self.m_sdk_info == other.m_sdk_info \
                   and self.m_exec_env == other.m_exec_env


class OutputMessage:
    def __init__(self, save_path, ad_info, output_history_key):
        self.m_save_path: str = save_path
        self.m_ad_info: AdInfo = ad_info
        self.m_output_history_key: OutputHistoryKey = output_history_key


class Output(metaclass=SingletonType):
    def __init__(self):
        self.m_ad_plugin_output_history: Dict[OutputHistoryKey, AdPluginOutput] = dict()
        self.m_message_queue: Queue = Queue()
        threading.Thread(target=self.thread_persist).start()

    def persist(self, ad_info: AdInfo, apk_info: ApkInfo, sdk_info: AdSdkInfo, save_path: str):
        Log.info('保存广告信息:{}', save_path)
        output_history_key = OutputHistoryKey(sdk_info, apk_info, Runtime().exec_env)
        if output_history_key not in self.m_ad_plugin_output_history:
            ad_plugin_output = AdPluginOutput()
            ad_plugin_output.apk_info = apk_info
            ad_plugin_output.sdk_info = sdk_info
            ad_plugin_output.exec_env = Runtime().exec_env
            self.m_ad_plugin_output_history[output_history_key] = ad_plugin_output
        self.m_message_queue.put(OutputMessage(save_path, ad_info, output_history_key))

    def __persist(self, output_message: OutputMessage):
        with open(output_message.m_save_path, 'w') as f:
            self.m_ad_plugin_output_history[output_message.m_output_history_key].ad_info_map[
                output_message.m_ad_info.uuid] = output_message.m_ad_info
            f.write(jsonpickle.encode(self.m_ad_plugin_output_history[output_message.m_output_history_key],
                                      indent=4, unpicklable=False))

    def thread_persist(self):
        while True:
            output_message = self.m_message_queue.get()
            Log.debug('received ad info')
            self.__persist(output_message)
