# coding=utf-8

import threading
import time
import traceback
from typing import List, AnyStr, Set, Iterable

from tweezer.resource.runtime import Runtime
from wisbec.android.adb import Adb
from wisbec.logging.log import Log


class TopAppMonitor:

    def __init__(self, dev_id, no_proxy_apps: List[AnyStr]):
        self.m_start_monitor = False
        self.m_thread_activating = False
        self.m_dev_id = dev_id
        self.m_no_proxy_apps: Set[AnyStr] = set(no_proxy_apps)
        self.m_user_installed_apps: Set[AnyStr] = Adb.get_user_installed_packages(self.m_dev_id)

    def add_no_proxy_app(self, no_proxy_app: str):
        self.m_no_proxy_apps.add(no_proxy_app)

    def add_no_proxy_apps(self, no_proxy_apps: Iterable[str]):
        self.m_no_proxy_apps.update(no_proxy_apps)

    def start_monitor(self, cb_on_switched):
        if self.m_start_monitor:
            pass
        elif self.m_thread_activating is False:
            self.m_start_monitor = True
            self.m_thread_activating = True
            threading.Thread(target=self.__thread_start_monitor,
                             args=(cb_on_switched,)).start()

    def __thread_start_monitor(self, cb_on_switched):
        last_pkg = ''
        Log.debug('user installed app is:')
        for user_installed_app in self.m_user_installed_apps:
            Log.debug(user_installed_app)
        while self.m_start_monitor:
            time.sleep(1)
            try:
                pkg = Adb.top_app(self.m_dev_id, Runtime().exec_env.sdk_level)
                if pkg is None:
                    Log.debug('top app is None')
                    time.sleep(0.5)
                    continue

                if last_pkg != pkg and pkg != 'null':
                    if pkg in self.m_no_proxy_apps:
                        Log.debug('{} is no proxy app.', pkg)
                        continue
                    elif pkg not in self.m_user_installed_apps:
                        Log.debug('{} is not user installed app.', pkg)
                        continue
                    else:
                        cb_on_switched(pkg)
                        last_pkg = pkg
            except Exception as e:
                traceback.print_exc()
                pass
        self.m_thread_activating = False

    def stop_monitor(self):
        self.m_start_monitor = False
        while self.m_thread_activating:
            time.sleep(0.1)
        pass
