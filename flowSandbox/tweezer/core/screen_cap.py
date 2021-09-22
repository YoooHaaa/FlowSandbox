# coding=utf-8

import os
import threading
import time

from wisbec.android.adb import Adb
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log


class ScreenCap:
    s_lock = threading.Lock()

    @staticmethod
    def __capture(device_id: str, save_path: str):
        with ScreenCap.s_lock:
            screenshot_device_path = '/sdcard/tweezer_screenshot.png'
            if Adb.screen_cap(device_id, screenshot_device_path) is False:
                Log.error('截屏失败, 保存记录失败！')
                return False
            FilesystemUtil.create_directories(os.path.dirname(save_path))
            if Adb.pull(device_id, screenshot_device_path, save_path) is False:
                Log.error('截屏文件拉取失败, 保存记录失败！')
                return False
            Log.info('截图完成:{}', save_path)
        return True

    @staticmethod
    def capture(device_id: str, save_path: str):
        ScreenCap.__capture(device_id, save_path)

    @staticmethod
    def delay_capture(device_id: str, save_path: str, delay_time: int):
        time.sleep(delay_time)
        return ScreenCap.capture(device_id, save_path)

    @staticmethod
    def capture_without_wait(device_id: str, save_path: str):
        if ScreenCap.s_lock.locked():
            return
        ScreenCap.__capture(device_id, save_path)
