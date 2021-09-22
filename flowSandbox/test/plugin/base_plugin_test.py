# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : base_plugin_test.py
# Time       ：2020/10/13 10:31
# Author     ：Rodney Cheung
"""
import os
from typing import List

from wisbec.logging.log import Log

from tweezer.config.config import Configor
from tweezer.resource import resource
from tweezer.resource.resource import CwdResource


class BasePluginTest:
    @staticmethod
    def init():
        resource.copy_resources_to_cwd()
        Configor.load_config()
        Log.init_logger(log_dir=CwdResource.get_log_path())

    @staticmethod
    def destroy():
        resource.remove_resources_from_cwd()

    @staticmethod
    def get_test_data_path() -> str:
        test_root_path_component: List[str] = list()
        for path_component in os.getcwd().split(os.path.sep):
            if path_component != 'test':
                test_root_path_component.append(path_component)
            else:
                test_root_path_component.append(path_component)
                break
        test_root_path = os.path.sep.join(test_root_path_component)
        return os.path.join(test_root_path, 'testdata')
