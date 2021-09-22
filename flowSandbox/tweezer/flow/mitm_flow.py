#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import threading

from mitmproxy import io, http
import json
import time
import requests
from typing import List
from mitmproxy import http
from tweezer.util.output import OutputUtil
from wisbec.logging.log import Log

class MitmFlow():

    def __init__(self, flow_path):
        self.m_replay_response_list: List[str] = []
        self.m_flow_path:str = flow_path
        self.m_flow_all: List[http.HTTPFlow] = []
        self.m_replay_over: bool = False
        self.__read_mitm()
        self.m_replay_save_file_lock = threading.Lock()
        threading.Thread(target=self.__thread_save_replay).start()


    def replay_flow(self):
        try:
            flow = self.__get_choose_request()
            self.__replay_flow(flow)
            self.m_replay_over = True
        except Exception as err:
            Log.error(str(err))
            exit(0)


    def __get_choose_request(self) -> http.HTTPFlow:
        flow = None
        user_input = input("请输入要重放的域名信息：")
        while flow == None:
            flow = self.__match_host(user_input)
            if not flow:
                user_input = input("未找到相关域名信息，请检查并重新输入：")
        return flow


    def __match_host(self, input_url:str) -> http.HTTPFlow:
        tmp_flow = []
        num = 1
        for flow in self.m_flow_all:
            if self.get_url(flow).find(input_url) != -1:
                tmp_flow.append(flow)
        if len(tmp_flow) == 0:
            return None
        elif len(tmp_flow) == 1:
            return tmp_flow[num - 1]
        else:
            print('匹配到的请求信息如下：')
            for flow in tmp_flow:
                print("[ " + str(num) + ' ] : ' + self.get_url(flow))
                num += 1
                print(os.linesep)
            choose = input("请输入序号，选择重放的请求")
            return tmp_flow[int(choose) - 1]



    def __get_replay_save_path(self):
        return self.m_flow_path[0:self.m_flow_path.rfind('\\')] + '\\replay.json'


    def __read_mitm(self):
        with open(self.m_flow_path, "rb") as f:
            for flow in io.FlowReader(f).stream():
                self.m_flow_all.append(flow)


    def __replay_flow(self, flow:http.HTTPFlow):
        num = int(input("请输入重放次数："))
        url = self.get_url(flow)
        headers = self.get_headers(flow)
        data = self.get_data(flow)
        while num:
            if (flow.request.method == 'GET'):
                try:
                    r = requests.get(url=url, headers=headers)
                    Log.info("GET Response:{}", r.text)
                    self.__append_replay_response(r.text)
                except Exception as err:
                    Log.error(str(err))
            elif(flow.request.method == 'POST'):
                try:
                    r = requests.post(url=url, headers=headers, data=data)
                    Log.info("POST Response:{}", r.text)
                    self.__append_replay_response(r.text)
                except Exception as err:
                    Log.error(str(err))
            num -= 1

    def get_headers(self, flow: http.HTTPFlow):
        return flow.request.headers


    def get_data(self, flow: http.HTTPFlow):
        return flow.request.content


    def get_url(self, flow: http.HTTPFlow) -> str:
        url = None
        try:
            url = flow.request.headers['host']
        except Exception as err:
            try:
                url = flow.request.get_state()["authority"].decode('utf8')
            except Exception as error:
                raise Exception('cannot get valid host')
        return flow.request.get_state()["scheme"].decode('utf-8') + '://' + url + flow.request.path


    def __thread_save_replay(self):
        while True:
            self.__replay_save_to_file()
            time.sleep(10)


    def __replay_save_to_file(self):
        with self.m_replay_save_file_lock:
            if len(self.m_replay_response_list) != 0 :
                OutputUtil.dump_replay_append(self.__get_replay_save_path(), self.m_replay_response_list)
                self.m_replay_response_list.clear()
            if self.m_replay_over and len(self.m_replay_response_list) == 0 :
                os._exit(0)


    def __append_replay_response(self, response: str):
        with self.m_replay_save_file_lock:
            self.m_replay_response_list.append(response)

    # print("1--" + str(flow.request.get_state()["authority"]))  # 域名，下面找不到，就用这个
    # print("2--" + str(flow.request.headers['host']))  # 域名,大多能找到
    # print("3--" + str(flow.request.host))  # 域名:180.97.104.187
    # print(flow.response.content.decode()) # 获取响应内容解码