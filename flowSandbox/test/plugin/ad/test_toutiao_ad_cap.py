# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_toutiao_ad_cap.py
# Time       ：11/4/20 09:12
# Author     ：Rodney Cheung
"""
import json
import os
import unittest

from test.plugin.base_plugin_test import BasePluginTest
from tweezer.plugins.ad.toutiao_ad_cap import ToutiaoAdCap


class TestToutiaoAdCap(unittest.TestCase, BasePluginTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.init()
        cls.m_test_data_path: str = os.path.join(cls.get_test_data_path(), 'plugin', 'ad', 'toutiao_ad_cap')
        cls.m_toutiao_ad_cap = ToutiaoAdCap()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.destroy()

    def test_decrypt_get_ad_response(self):
        toutiao_crypt_json_path = os.path.join(self.m_test_data_path, 'toutiao.json')
        with open(toutiao_crypt_json_path, 'rb') as f, \
                open(os.path.join(self.m_test_data_path, 'res.json'), 'w') as res:
            is_suc, data, err = self.m_toutiao_ad_cap._ToutiaoAdCap__decrypt_get_ad_response(json.load(f))
            self.assertEqual(is_suc, True)
            print(data, file=res)


if __name__ == '__main__':
    unittest.main()
