# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : main.py
# Time       ：2020/8/20 16:51
# Author     ：Rodney Cheung
"""
import argparse
import os
import sys

import pkg_resources

sys.path.append('../')

import tweezer
from tweezer.config.config import Configor
from tweezer.core.init import Init
from tweezer.core.upstream_proxy import UpstreamProxy
from tweezer.mitmdump_wrapper import mitmdump_main
from tweezer.model.params import Params
from tweezer.util.TerminateTweezer import TweezerTerminator
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log
from tweezer.flow.mitm_flow import MitmFlow


def exec_main_func(params: Params):
    tweezer_path = os.path.dirname(tweezer.__file__)
    mitm_script_path = os.path.join(tweezer_path, 'script', 'phone_script.py')
    if not FilesystemUtil.is_file_exist(mitm_script_path):
        print(mitm_script_path)

    cmd_lines = ['-p', params.proxy_port,
                 '-s', mitm_script_path ]
    cmd_lines += ['--mode', 'upstream:http://{}:{}/'.format('127.0.0.1', Configor.get_loopback_upstream_port())]
    cmd_lines += ['-k']

    # subprocess.run(cmd_lines)
    mitmdump_main(*cmd_lines)


def exec_flow_func(params: Params):
    MitmFlow(params.flow).replay_flow()



def init_all():
    Init().init_config()
    Init().init_log()
    Init().init_adb()
    Init().init_device()
    Init().init_output_dir()
    Init().init_exec_dev_info()
    Init().init_jsonpickle()


def init_small():
    Init().init_config()
    Init().init_log()
    # Init().init_adb()
    # Init().init_device()
    # Init().init_output_dir()
    # Init().init_exec_dev_info()
    # Init().init_jsonpickle()

def get_params() -> Params:
    parser = argparse.ArgumentParser(description='Dynamic Sandbox')
    parser.add_argument('-p', '--port',
                        default='8000',
                        type=str,
                        help='Proxy service port',
                        dest='port')
    parser.add_argument('-v', '--version',
                        default=False,
                        action="store_true",
                        help="show tweezer version",
                        dest='version')
    parser.add_argument('-f', '--flow',
                        default="",
                        type=str,
                        help="replay flow",
                        dest='flow')
    args = parser.parse_known_args()
    port = args[0].port
    version = args[0].version
    flow = args[0].flow
    return Params(port, version, flow)


def main():
    params = get_params()
    if params.version:
        try:
            pc_tool_version = pkg_resources.get_distribution('tweezer')
            print(pc_tool_version)
        except Exception as err:
            Log.error(str(err))
        return
    TweezerTerminator.instance().init()
    TweezerTerminator.instance().register_term_sign()
    if params.flow:
        init_small()
        exec_flow_func(params)
    else:
        init_all()
        mitmdump_path = Init().init_mitm()
        if mitmdump_path == '':
            return
        if UpstreamProxy.instance().start_loopback_proxy() is False:
            Log.error('启动本地proxy代理失败, 请检查端口是否被占用: {}'.format(Configor.get_loopback_upstream_port()))
            exit(0)
        exec_main_func(params)



if __name__ == '__main__':
    main()
