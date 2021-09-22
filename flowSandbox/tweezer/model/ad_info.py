# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : ad_info.py
# Time       ：2020/9/8 14:25
# Author     ：Rodney Cheung
"""
import uuid
from enum import Enum
from typing import List, Dict

from tweezer.util.wrapper import now


class AdType(Enum):
    NONE = 0
    BANNER = 1
    SPLASH = 2


class AdEvidence:
    def __init__(self):
        self.__title: str = ''
        self.__description: str = ''
        self.__ad_url: str = ''
        self.__ad_screenshot_path: str = ''
        self.__ad_pic_url_list: List[str] = list()
        self.__ad_pic_path_map: Dict[str, List[str]] = dict()
        self.__ad_flow_path: str = ''

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    @property
    def ad_url(self):
        return self.__ad_url

    @ad_url.setter
    def ad_url(self, value):
        self.__ad_url = value

    @property
    def ad_screenshot_path(self):
        return self.__ad_screenshot_path

    @ad_screenshot_path.setter
    def ad_screenshot_path(self, value):
        self.__ad_screenshot_path = value

    @property
    def ad_pic_url_list(self):
        return self.__ad_pic_url_list

    @ad_pic_url_list.setter
    def ad_pic_url_list(self, value):
        self.__ad_pic_url_list = value

    @property
    def ad_pic_path_map(self):
        return self.__ad_pic_path_map

    @property
    def ad_flow_path(self):
        return self.__ad_flow_path

    @ad_flow_path.setter
    def ad_flow_path(self, value):
        self.__ad_flow_path = value

    def __getstate__(self):
        state = {
            '标题': self.__title,
            '描述': self.__description,
            '广告URL': self.__ad_url,
            '广告截图URL': self.__ad_screenshot_path,
            '广告图片URL列表': self.__ad_pic_url_list,
            '广告图片存放路径': self.__ad_pic_path_map,
            '广告网络包': self.__ad_flow_path
        }
        return state

    def get_ad_pic_path(self, pic_type: str) -> str:
        if pic_type not in self.__ad_pic_path_map:
            return ''
        return self.__ad_pic_path_map[pic_type][-1]

    def set_ad_pic_path(self, pic_type: str, pic_path: str):
        if pic_type not in self.__ad_pic_path_map:
            self.__ad_pic_path_map[pic_type] = list()
        self.__ad_pic_path_map[pic_type].append(pic_path)


class OptionalAdEvidence:
    def __init__(self):
        self.__ad_width: int = 0
        self.__ad_height: int = 0
        self.__cooperation_name: str = ''
        self.__ad_slot_id: str = ''
        self.__ad_type: AdType = AdType.NONE
        self.__ad_scene: str = ''

    @property
    def ad_width(self):
        return self.__ad_width

    @ad_width.setter
    def ad_width(self, value):
        self.__ad_width = value

    @property
    def ad_height(self):
        return self.__ad_height

    @ad_height.setter
    def ad_height(self, value):
        self.__ad_height = value

    @property
    def cooperation_name(self):
        return self.__cooperation_name

    @cooperation_name.setter
    def cooperation_name(self, value):
        self.__cooperation_name = value

    @property
    def ad_slot_id(self):
        return self.__ad_slot_id

    @ad_slot_id.setter
    def ad_slot_id(self, value):
        self.__ad_slot_id = value

    @property
    def ad_type(self):
        return self.__ad_type

    @ad_type.setter
    def ad_type(self, value):
        self.__ad_type = value

    @property
    def ad_scene(self):
        return self.__ad_scene

    @ad_scene.setter
    def ad_scene(self, value):
        self.__ad_scene = value

    def __getstate__(self):
        state = {
            '长度': self.__ad_height,
            '宽度': self.__ad_width,
            '公司名': self.__cooperation_name,
            '广告位ID': self.__ad_slot_id,
            '广告类型': self.__ad_type.name,
            '广告场景': self.__ad_scene
        }
        return state


class AdInfo:
    def __init__(self, ad_evidence=None,
                 optional_ad_evidence=None):
        self.__cap_time: str = now()
        self.__uuid: str = str(uuid.uuid1())
        self.__ad_evidence: AdEvidence = ad_evidence
        self.__optional_ad_evidence: OptionalAdEvidence = optional_ad_evidence

    @property
    def cap_time(self):
        return self.__cap_time

    @cap_time.setter
    def cap_time(self, value):
        self.__cap_time = value

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, value):
        self.__uuid = value

    @property
    def ad_evidence(self):
        return self.__ad_evidence

    @ad_evidence.setter
    def ad_evidence(self, value):
        self.__ad_evidence = value

    @property
    def optional_ad_evidence(self):
        return self.__optional_ad_evidence

    @optional_ad_evidence.setter
    def optional_ad_evidence(self, value):
        self.__optional_ad_evidence = value

    def __getstate__(self):
        state = {
            '抓取时间': self.__cap_time,
            'uuid': self.__uuid,
            '广告取证': self.__ad_evidence,
            '可选广告信息': self.__optional_ad_evidence
        }
        return state
