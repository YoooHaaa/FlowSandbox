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


class HotkeyScreenCap(BaseHotkeyPlugin):

    def register_event(self):
        RuntimeEvent().reg_event(event_type=RuntimeEventType.SWITCHED_APP, callback=self.__cb_switched_app)

    def run(self):
        self.register_event()

    def __init__(self):
        BaseHotkeyPlugin.__init__(self)
        self.m_top_app = ''
        self.m_saving = False
        self.m_hotkey_screen_cap_conf = Configor.get_hotkey_screen_cap_conf()
        self.__register_system_key_bind()

    def __thread_screen_cap(self):
        if self.m_top_app == '':
            Log.error('顶层没有有效的应用, 无法保存！')
            self.m_saving = False
            return False

        Log.info('正在截图中....')
        output_dir = os.path.join(CwdResource.get_plugin_output_path(), constant.SCREENSHOT_OUTPUT_DIR, self.m_top_app)
        FilesystemUtil.create_directories(output_dir)
        # screencap
        output_path = os.path.join(output_dir, '{}.png'.format(now()))
        if ScreenCap.capture(Runtime().device_id, output_path) is False:
            self.m_saving = False
            return False
        Log.info('截屏保存成功： {}', output_path)
        self.m_saving = False
        return True

    def __register_system_key_bind(self):
        shortcut = self.m_hotkey_screen_cap_conf['shortcut']
        if shortcut == 'default':
            if system.is_mac_os():
                shortcut = 'command+s'
            else:
                shortcut = 'alt+s'
        if self.is_shortcut_valid(shortcut):
            keyboard.add_hotkey(shortcut, self.__screen_cap)
            Log.info("热键注册成功, 按下{}进行截屏", shortcut)
        else:
            Log.error("热键{}绑定不可用，请重新设置或使用默认设置", shortcut)

    def __screen_cap(self):
        if self.m_saving:
            return
        self.m_saving = True
        self.__thread_screen_cap()

    def __cb_switched_app(self, event_type, **kwargs):
        self.m_top_app = kwargs['pkg']
