# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_tuia_ad_cap.py
# Time       ：2020/9/11 09:38
# Author     ：Rodney Cheung
"""
import unittest

from tweezer.plugins.ad.tuia_ad_cap import TuiaAdCap


class TestTuiaAdCap(unittest.TestCase):
    def test_self_increasing_screen_cap_name(self):
        print(TuiaAdCap.self_increasing_screen_cap_name('/Users/jsrdzhk/ad_screenshot_120.png'))


if __name__ == '__main__':
    unittest.main()
