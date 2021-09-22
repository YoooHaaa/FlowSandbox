import threading
from typing import Dict, Set, Callable

from wisbec.design_patterns.singleton import SingletonType

from enum import Enum


class RuntimeEventType(Enum):
    SWITCHED_APP = 1
    REQUEST = 80
    RESPONSE = 81


class RuntimeEvent(metaclass=SingletonType):
    def __init__(self):
        self.m_events_data = {}  # {event_type, dict_data},  最新的事件数据(最后一次)
        self.m_callbacks: Dict[RuntimeEventType, Set[Callable]] = {}
        self.m_lock = threading.Lock()
        self.__init_m_callbacks()

    def __init_m_callbacks(self):
        for event_type in RuntimeEventType:
            self.m_callbacks[event_type] = set()

    def on_event(self, event_type, **kwargs):
        with self.m_lock:
            self.m_events_data[event_type] = kwargs
            if event_type in self.m_callbacks:
                for cb_fun in self.m_callbacks[event_type]:
                    cb_fun(event_type, **kwargs)

    # callback: cb(event_type, **kwargs)
    def reg_event(self, event_type, callback):
        with self.m_lock:
            self.m_callbacks[event_type].add(callback)

    def unreg_event(self, event_type: RuntimeEventType, callback: Callable):
        with self.m_lock:
            if event_type not in self.m_callbacks:
                return
            self.m_callbacks[event_type].discard(callback)

    # return: dict_data or None
    def get_last_event(self, event_type):
        with self.m_lock:
            if event_type in self.m_events_data:
                return self.m_events_data[event_type]
            return None
        pass
