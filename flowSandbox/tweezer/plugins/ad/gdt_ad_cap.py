# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : gdt_ad_cap.py
# Time       ：2020/9/7 16:13
# Author     ：Rodney Cheung
"""
import json
import os
import re
from typing import Dict
from urllib import parse

from mitmproxy import http

from tweezer.config.config import Configor
from tweezer.core.runtime_event import RuntimeEvent, RuntimeEventType
from tweezer.model.ad_info import AdInfo, AdType, AdEvidence, OptionalAdEvidence
from tweezer.model.ad_sdk import AdSdkInfo, AdSdkType
from tweezer.plugins.base.base_ad_plugin import BaseAdPlugin
from tweezer.util.output import OutputUtil
from tweezer.util.wrapper import dict_get
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log


class GdtAdCap(BaseAdPlugin):

    def load_conf(self):
        conf = Configor.get_ad_cap_conf(AdSdkType.gdt)
        self.m_screen_cap_delay_time = conf['capture_delay_time']

    def get_sdk_info(self):
        self.m_sdk_info = AdSdkInfo(AdSdkType.gdt.chinese_name(), '0.1')

    def register_event(self):
        RuntimeEvent().reg_event(event_type=RuntimeEventType.REQUEST, callback=self.__cb_request)
        RuntimeEvent().reg_event(event_type=RuntimeEventType.RESPONSE, callback=self.__cb_response)
        RuntimeEvent().reg_event(event_type=RuntimeEventType.SWITCHED_APP, callback=self.__cb_switch_app)

    def run(self):
        self.register_event()

    def __init__(self):
        super().__init__()
        self.m_matched_url_map: Dict[str, AdInfo] = dict()
        self.m_ad_info_map: Dict[str, AdInfo] = dict()

    def __cb_switch_app(self, event_type, **kwargs):
        self.m_top_app = kwargs['pkg']
        self.flush_app_info()

    def __cb_request(self, event_type, **kwargs):
        flow: http.HTTPFlow = kwargs['flow']
        if self.__parse_get_ad_info_request_params_get(flow):
            return
        if self.__parse_get_ad_info_request_params_post(flow):
            return

    def __cb_response(self, event_type, **kwargs):
        flow: http.HTTPFlow = kwargs['flow']
        if self.__parse_gdt_ad_response(flow):
            return
        if self.__match_ad_url_access(flow):
            return

    def __parse_gdt_ad_response_impl(self, loaded: dict, ad_info: AdInfo):
        fmt_json = json.dumps(loaded, indent=4, ensure_ascii=False)
        if 'data' not in loaded:
            Log.error('回包格式错误:no data found')
            self.persist_err_content(fmt_json, self.get_err_save_path('gdt_err_response.txt'))
            return
        data = loaded['data']
        if ad_info.optional_ad_evidence.ad_slot_id not in data:
            Log.error('回包格式错误:ad slot not matched')
            self.persist_err_content(fmt_json, self.get_err_save_path('gdt_err_response.txt'))
            return
        pos_id_ads = data[ad_info.optional_ad_evidence.ad_slot_id]
        ret_code = dict_get(data, 'ret')
        if ret_code != 0:
            msg = dict_get(data, 'msg')
            if msg is not None:
                Log.info('广点通广告加载错误:{}', msg)
                return
        if 'list' not in pos_id_ads:
            Log.error('回包格式错误:no ad list found')
            self.persist_err_content(fmt_json, self.get_err_save_path('gdt_err_response.txt'))
            return
        preload_ad_list = pos_id_ads['list']
        if len(preload_ad_list) == 0:
            self.persist_err_content(fmt_json, self.get_err_save_path('gdt_err_response.txt'))
        for preload_ad in preload_ad_list:
            ad_evidence = AdEvidence()
            ad_pic_url = dict_get(preload_ad, 'img')
            if ad_pic_url is not None and ad_pic_url != '':
                ad_evidence.ad_pic_url_list.append(ad_pic_url)
            cooperation_logo_path = dict_get(preload_ad, 'img2')
            if cooperation_logo_path is not None and cooperation_logo_path != '':
                ad_evidence.ad_pic_url_list.append(cooperation_logo_path)
            ad_evidence.title = dict_get(preload_ad, 'txt')
            ad_evidence.description = dict_get(preload_ad, 'desc')
            rl = dict_get(preload_ad, 'rl')
            if rl is not None and rl != '':
                ad_evidence.ad_url = rl
                self.m_ad_info_map[rl] = ad_info
            ad_info.ad_evidence = ad_evidence
            optional_ad_evidence = OptionalAdEvidence()
            optional_ad_evidence.cooperation_name = dict_get(preload_ad, 'corporation_name')
            ad_info.optional_ad_evidence = optional_ad_evidence
            self.persist_ad_info(ad_info)

    def __parse_gdt_ad_response(self, flow: http.HTTPFlow) -> bool:
        url = flow.request.url
        if url not in self.m_matched_url_map:
            return False
        else:
            flow.response.decode()
            if flow.response.content is None:
                Log.error('广告响应体转码错误')
                return False
            loaded = json.loads(flow.response.content)
            ad_info = self.m_matched_url_map[url]
            self.__parse_gdt_ad_response_impl(loaded, ad_info)
            return True

    def __parse_get_ad_info_request_params_impl(self, url: str, params: dict):
        optional_ad_evidence = OptionalAdEvidence()
        if 'posid' in params:
            optional_ad_evidence.ad_slot_id = params['posid'][0]
        if 'posh' in params and 'posw' in params:
            optional_ad_evidence.ad_width = params['posh'][0]
            optional_ad_evidence.ad_height = params['posw'][0]
            optional_ad_evidence.ad_type = AdType.SPLASH
        else:
            optional_ad_evidence.ad_type = AdType.BANNER
        self.m_matched_url_map[url] = AdInfo(optional_ad_evidence=optional_ad_evidence)

    # parse request params of http get
    def __parse_get_ad_info_request_params_get(self, flow: http.HTTPFlow) -> bool:
        url = flow.request.url
        url_pattern = re.compile(r'https://mi\.gdt\.qq\.com/gdt_mview\.fcg.+')
        if url_pattern.fullmatch(url):
            res = parse.urlparse(url)
            params = parse.parse_qs(res.query)
            self.__parse_get_ad_info_request_params_impl(url, params)
            return True
        return False

    def __parse_get_ad_info_request_params_post(self, flow: http.HTTPFlow) -> bool:
        url = flow.request.url
        url_pattern = re.compile(r'https://mi\.gdt\.qq\.com/gdt_mview\.fcg')
        if url_pattern.fullmatch(url):
            params = parse.parse_qs(flow.request.content.decode())
            self.__parse_get_ad_info_request_params_impl(url, params)
            return True
        return False

    def __match_ad_url_access(self, flow: http.HTTPFlow) -> bool:
        url = flow.request.url
        if url not in self.m_ad_info_map:
            return False
        ad_info = self.m_ad_info_map[url]
        evidence_save_path = os.path.join(self.get_output_path(), ad_info.uuid)
        FilesystemUtil.create_directories(evidence_save_path)
        screenshot_path = os.path.join(evidence_save_path, 'ad_screenshot_0.png')
        ad_info.ad_evidence.set_ad_pic_path('screenshot', screenshot_path)
        self.thread_screen_cap(screenshot_path)
        ad_flow_path = os.path.join(evidence_save_path, 'ad_net_pkg_0.mitm')
        ad_info.ad_evidence.ad_flow_path = ad_flow_path
        OutputUtil.dump_flow(ad_flow_path, flow)
        self.persist_ad_info(ad_info)
        return True

    @staticmethod
    def __save_img(file_name: str, flow: http.HTTPFlow):
        FilesystemUtil.create_directories(os.path.dirname(file_name))
        with open(file_name, 'wb+') as f:
            f.write(flow.response.content)
