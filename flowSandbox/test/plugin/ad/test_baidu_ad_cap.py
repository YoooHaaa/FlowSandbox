# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_baidu_ad_cap.py
# Time       ：11/1/20 10:30
# Author     ：Rodney Cheung
"""
import os
import unittest

from test.plugin.base_plugin_test import BasePluginTest
from tweezer.plugins.ad.baidu_ad_cap import BaiduAdCap


class TestBadiuAdCap(unittest.TestCase, BasePluginTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.init()
        cls.m_test_data_path: str = os.path.join(cls.get_test_data_path(), 'plugin', 'ad', 'baidu_ad_cap')
        cls.m_baidu_ad_cap = BaiduAdCap()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.destroy()

    def test_get_ad_json_from_html_content(self):
        with open(os.path.join(self.m_test_data_path, 'raw_response.html'), 'r') as f:
            print(self.m_baidu_ad_cap.get_ad_json_from_html_content(f.read()))


if __name__ == '__main__':
    unittest.main()
