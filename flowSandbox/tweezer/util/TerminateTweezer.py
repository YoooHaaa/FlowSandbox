# coding=utf-8

import os
import signal

import psutil
import traceback

from wisbec import system
from wisbec.logging.log import Log


class TweezerTerminator:
    s_instance = None
    m_main_threading: psutil.Process = None

    def __init__(self):
        caller = traceback.extract_stack()[-2][2]
        assert caller == 'instance', "Please use {}.get_instance() got it.".format(TweezerTerminator.__name__)
        pass

    @classmethod
    def instance(cls):
        # 每个adb 1个单例
        if cls.s_instance is None:
            cls.s_instance = cls()
        return cls.s_instance

    # 在主进程调用，以便搜集所有子进程信息
    def init(self):
        if self.m_main_threading:
            return

        self.m_main_threading = psutil.Process()

    def register_term_sign(self):
        signal.signal(signal.SIGINT, self.__sigint_handler)
        signal.signal(signal.SIGTERM, self.__sigint_handler)
        if not system.is_windows():
            signal.signal(signal.SIGHUP, self.__sigint_handler)

    def terminate(self):
        if self.m_main_threading is None:
            return

        if system.is_windows():
            kill_sig = signal.SIGILL
        else:
            kill_sig = signal.SIGKILL

        children = self.m_main_threading.children(recursive=True)
        for child in children:
            if self.m_main_threading.pid != child.pid:
                try:
                    os.kill(child.pid, kill_sig)
                except:
                    pass
                # print('os.kill: {}'.format(child.pid))
        try:
            os.kill(self.m_main_threading.pid, kill_sig)
        except:
            pass

    def __sigint_handler(self, signum, frame):
        # Log.warning('terminate tweezer...')
        self.terminate()