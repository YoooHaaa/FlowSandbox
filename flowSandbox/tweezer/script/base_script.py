# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : base_script.py
# Time       ：2020/10/20 18:08
# Author     ：Rodney Cheung
"""
import base64
import os
from mitmproxy import http
import json
from tweezer.core.runtime_event import RuntimeEventType, RuntimeEvent
from tweezer.core.upstream_proxy import UpstreamProxy
from tweezer.util.TerminateTweezer import TweezerTerminator
from tweezer.util.log import LogUtil


class BaseScript:
    @staticmethod
    def gen_auth_token(user, pwd):
        #  proxy_data = urlparse('http://sandbox:7481590263@39.104.55.246:8888')
        user_pwd = user + ':' + pwd
        auth_token = "Basic" + " " + base64.b64encode(user_pwd.encode()).decode()
        return auth_token

    def request(self, flow: http.HTTPFlow):
        print("************************* < request > ************************")
        try:
            host, port, user, pwd = UpstreamProxy.instance().get_upstream_proxy()
            # print(host, port, user, pwd)
            flow.live.change_upstream_proxy_server((host, port))
            if user and pwd:
                flow.request.headers["Proxy-Authorization"] = self.gen_auth_token(user, pwd)
            # if self.__is_known_ad_platform(c_flow.request.url):
            #     if Configor.get_tweezer_conf()['is_drop_known_ad_platform_flow']:
            #         flow.response = http.HTTPResponse.make(
            #             status_code=500
            #         )
            #         return
            RuntimeEvent().on_event(RuntimeEventType.REQUEST, flow=flow)
        except Exception as e:
            LogUtil.critical_exception(e)

    def response(self, flow: http.HTTPFlow):
        print("************************* < response > ************************")
        try:
            RuntimeEvent().on_event(RuntimeEventType.RESPONSE, flow=flow)
        except Exception as e:
            LogUtil.critical_exception(e)


TweezerTerminator.instance().register_term_sign()
