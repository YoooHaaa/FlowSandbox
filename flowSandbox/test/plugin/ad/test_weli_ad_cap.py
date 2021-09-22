# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_weli_ad_cap.py
# Time       ：2020/10/13 10:02
# Author     ：Rodney Cheung
"""
import json
import os
import unittest

from test.plugin.base_plugin_test import BasePluginTest
from tweezer.plugins.ad.weli_ad_cap import WeliAdCap


class TestWeliAdCap(unittest.TestCase, BasePluginTest):
    @classmethod
    def setUpClass(cls):
        cls.init()
        cls.m_weli_ad_cap = WeliAdCap()
        cls.m_test_data_path=os.path.join(cls.get_test_data_path(), 'plugin', 'ad', 'weli_ad_cap')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.destroy()

    def test_parse_coin_ads(self):
        coin_ads_json_path = os.path.join(self.m_test_data_path, 'coin_ads.json')
        with open(coin_ads_json_path) as f:
            self.m_weli_ad_cap._WeliAdCap__parse_coin_ads_impl(json.load(f))

    def test_parse_ads_pool(self):
        ads_pool_json_path = os.path.join(self.m_test_data_path, 'ads_pool.json')
        with open(ads_pool_json_path) as f:
            self.m_weli_ad_cap._WeliAdCap__parse_ad_pools_response_impl(json.load(f))

    def test_parse_zhwnl_ad_1_impl(self):
        zhwnl_1_json_path = os.path.join(self.m_test_data_path, 'zhwnl_1.json')
        with open(zhwnl_1_json_path) as f:
            self.m_weli_ad_cap._WeliAdCap__parse_zhwnl_ad_1_impl(json.load(f))

    def test_parse_zhwnl_ad_2_impl(self):
        zhwnl_2_json_path = os.path.join(self.m_test_data_path, 'zhwnl_2.json')
        with open(zhwnl_2_json_path) as f:
            self.m_weli_ad_cap._WeliAdCap__parse_zhwnl_ad_2_impl(json.load(f))

    def test_parse_ad_get_impl(self):
        ad_get_json_path = os.path.join(self.m_test_data_path, 'ad_get.json')
        with open(ad_get_json_path) as f:
            self.m_weli_ad_cap._WeliAdCap__parse_ad_get_impl(json.load(f))


if __name__ == '__main__':
    unittest.main()
