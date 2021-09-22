# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_gdt_ad_cap.py
# Time       ：2020/10/13 15:47
# Author     ：Rodney Cheung
"""
import json
import os
import unittest

from test.plugin.base_plugin_test import BasePluginTest
from tweezer.model.ad_info import AdInfo, OptionalAdEvidence
from tweezer.plugins.ad.gdt_ad_cap import GdtAdCap


class TestGdtAdCap(unittest.TestCase, BasePluginTest):
    @classmethod
    def setUpClass(cls) -> None:
        cls.init()
        cls.m_test_data_path: str = os.path.join(cls.get_test_data_path(), 'plugin', 'ad', 'gdt_ad_cap')
        cls.m_gdt_ad_cap = GdtAdCap()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.destroy()

    def test_parse_gdt_ad_response_impl(self):
        gdt_ad_response_json_path = os.path.join(self.m_test_data_path, 'gdt_ad_response.json')
        with open(gdt_ad_response_json_path) as f:
            loaded = json.load(f)
            ad_info = AdInfo(optional_ad_evidence=OptionalAdEvidence())
            ad_info.optional_ad_evidence.ad_slot_id = '7071739686784189'
            self.m_gdt_ad_cap._GdtAdCap__parse_gdt_ad_response_impl(loaded, ad_info)


if __name__ == '__main__':
    unittest.main()
