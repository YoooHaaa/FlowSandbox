# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : base_hotkey_plugin.py
# Time       ：2020/9/4 09:52
# Author     ：Rodney Cheung
"""
import abc

from tweezer.plugins.base.base_plugin import BasePlugin
from tweezer.util import hotkey


class BaseHotkeyPlugin(BasePlugin, metaclass=abc.ABCMeta):
    def __init__(self):
        BasePlugin.__init__(self)

    @staticmethod
    def is_shortcut_valid(shortcut: str) -> bool:
        invalid_hotkeys = hotkey.get_invalid_hotkey()
        for invalid_hotkey in invalid_hotkeys:
            if invalid_hotkey in shortcut:
                return False
        return True
