# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : flow_cap.py
# Time       ：11/27/20 09:42
# Author     ：Rodney Cheung
"""
import os
import threading
import time
from typing import List

from mitmproxy import http

from tweezer.core.runtime_event import RuntimeEvent, RuntimeEventType
from tweezer.plugins.base.base_plugin import BasePlugin
from tweezer.resource.resource import CwdResource
from tweezer.util.output import OutputUtil
from wisbec.filesystem.filesystem import FilesystemUtil


class FlowCap(BasePlugin):
    def run(self):
        self.register_event()

    def register_event(self):
        RuntimeEvent().reg_event(event_type=RuntimeEventType.RESPONSE, callback=self.__cb_response)
        RuntimeEvent().reg_event(event_type=RuntimeEventType.SWITCHED_APP, callback=self.__cb_switch_app)

    def __init__(self):
        super().__init__()
        self.m_mitm_flow_list: List[http.HTTPFlow] = list()
        self.m_flow_save_file_lock = threading.Lock()
        threading.Thread(target=self.__thread_save).start()

    def __del__(self):
        self.__flow_save_to_file()

    def __cb_response(self, event_type, **kwargs):
        flow: http.HTTPFlow = kwargs['flow']
        self.__append_flow(flow)

    def __cb_switch_app(self, event_type, **kwargs):
        if self.m_apk_info is not None:
            self.__flow_save_to_file()
        self.m_top_app = kwargs['pkg']
        self.flush_app_info()

    def __append_flow(self, flow: http.HTTPFlow):
        with self.m_flow_save_file_lock:
            self.m_mitm_flow_list.append(flow)

    def __get_flows_save_path(self):
        flow_save_dir = os.path.join(CwdResource.get_output_path(), self.m_apk_info.app_name)
        FilesystemUtil.create_directories(flow_save_dir)
        flow_save_path = os.path.join(flow_save_dir, 'flow.mitm')
        return flow_save_path

    def __flow_save_to_file(self):
        with self.m_flow_save_file_lock:
            if len(self.m_mitm_flow_list) != 0 and self.m_apk_info is not None:
                OutputUtil.dump_flows_append(self.__get_flows_save_path(), self.m_mitm_flow_list)
                self.m_mitm_flow_list.clear()

    def __thread_save(self):
        while True:
            self.__flow_save_to_file()
            time.sleep(10)
