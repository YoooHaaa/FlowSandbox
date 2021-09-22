# coding=utf-8

import os
import shutil
from typing import List

from mitmproxy import io, http
from wisbec.file.file import FileUtil
from wisbec.logging.log import Log
import json
from tweezer.util.wrapper import now


class OutputUtil:

    @staticmethod
    def dump_flow(path: str, flow: http.HTTPFlow):
        with open(path, 'wb+') as f:
            io.FlowWriter(f).add(flow)

    @staticmethod
    def dump_flow_append(path: str, flow: http.HTTPFlow):
        with open(path, "ab") as f:
            io.FlowWriter(f).add(flow)

    @staticmethod
    def dump_flows_append(path: str, flows: List[http.HTTPFlow]):
        with open(path, "ab") as f:
            for flow in flows:
                io.FlowWriter(f).add(flow)

    @staticmethod
    def dump_replay_append(path: str, flows: list):
        with open(path, "ab") as f:
            for flow in flows:
                f.write("***************************************************************************************************\r\n".encode('utf-8'))
                f.write(flow.encode('utf-8'))
                f.write('\r\n'.encode('utf-8'))
                f.write('\r\n'.encode('utf-8'))

    @staticmethod
    def save_plugin_output(screenshots, url, match_category, flows, output_dir: str, comment=None):
        path_prefix = os.path.join(output_dir, '{}_'.format(match_category))

        # screenshot
        _now = now()
        for i in range(len(screenshots)):
            ss_path = screenshots[i]

            if len(screenshots) == 1:
                dst_screencap_file = path_prefix + '{}.png'.format(_now)
            else:
                dst_screencap_file = path_prefix + '{}-{}.png'.format(_now, i + 1)

            shutil.copy(ss_path, dst_screencap_file)

        # url
        url_file = path_prefix + '{}.txt'.format(_now)
        info = url
        if comment:
            info += '\n\n---------------------\n\n' + comment
        FileUtil.write_file(url_file, 'wb', info.encode())

        # flow dump
        dump_file = path_prefix + '{}.mitm'.format(_now)
        OutputUtil.dump_flows_append(dump_file, flows)
        Log.info("保存数据包记录： {}", dump_file)
