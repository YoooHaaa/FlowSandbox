# coding=utf-8

import os

import keyboard

from tweezer.core.runtime_event import RuntimeEvent, RuntimeEventType
from wisbec import system
from wisbec.android.adb import Adb
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log

from tweezer.config.config import Configor
from tweezer.core.screen_cap import ScreenCap
from tweezer.plugins.base.base_hotkey_plugin import BaseHotkeyPlugin
from tweezer.resource import constant
from tweezer.resource.resource import CwdResource
from tweezer.resource.runtime import Runtime
from tweezer.util.wrapper import now


class HotkeyExit(BaseHotkeyPlugin):

    def register_event(self):
        RuntimeEvent().reg_event(event_type=RuntimeEventType.SWITCHED_APP, callback=self.__cb_switched_app)

    def run(self):
        self.register_event()

    def __init__(self):
        BaseHotkeyPlugin.__init__(self)
        self.m_top_app = ''
        self.m_hotkey_exit_conf = Configor.get_hotkey_exit_conf()
        self.__register_system_key_bind()


    def __register_system_key_bind(self):
        shortcut = self.m_hotkey_exit_conf['shortcut']
        if shortcut == 'default':
            if system.is_mac_os():
                shortcut = 'command+e'
            else:
                shortcut = 'alt+e'
        if self.is_shortcut_valid(shortcut):
            keyboard.add_hotkey(shortcut, self.__exit_tweezer)
            Log.info("热键注册成功, 按下{}退出程序<退出程序后，手机将重启!>", shortcut)
        else:
            Log.error("热键{}绑定不可用，请重新设置或使用默认设置", shortcut)


    def __exit_tweezer(self):
        '''
        解除代理设置，重启手机，退出程序
        '''
        Adb.cancel_proxy()
        print("正在退出 tweezer... ...")
        os._exit(0) # 用于线程中退出


    def __cb_switched_app(self, event_type, **kwargs):
        self.m_top_app = kwargs['pkg']



