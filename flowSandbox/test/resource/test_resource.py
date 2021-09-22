# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : test_resource.py
# Time       ：2020/8/20 15:42
# Author     ：Rodney Cheung
"""
import unittest

from tweezer.resource.resource import CwdResource, PackageResource


class TestResource(unittest.TestCase):
    def test_get_plugin_path(self):
        print(PackageResource.get_plugin_path())

    def test_get_config_path(self):
        print(PackageResource.get_config_path())

    def test_get_rules_path(self):
        print(PackageResource.get_rules_path())

    def test_get_output_path(self):
        print(CwdResource.get_output_path())


if __name__ == '__main__':
    unittest.main()
