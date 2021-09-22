# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_config.py
# Time       ：2020/8/31 11:37
# Author     ：Rodney Cheung
"""
import unittest

from tweezer.config.config import Configor


class TestConfig(unittest.TestCase):
    def test_load_config(self):
        Configor.load_config()
        print(Configor.get_tweezer_conf()['plugins'])
        for ad_platform, is_block in Configor.get_known_ad_platforms_conf()['known_ad_platforms'].items():
            print(ad_platform, is_block)


if __name__ == '__main__':
    unittest.main()
