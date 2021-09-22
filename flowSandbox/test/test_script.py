# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_script.py
# Time       ：2020/9/1 17:43
# Author     ：Rodney Cheung
"""
import unittest

from tweezer.script.phone_script import PhoneScript


class TestDispatcher(unittest.TestCase):
    def test_phone_script(self):
        PhoneScript()


if __name__ == '__main__':
    unittest.main()
