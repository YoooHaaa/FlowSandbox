# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : init.py
# Time       ：11/4/20 15:01
# Author     ：Rodney Cheung
"""
import logging
import os

import jsonpickle

from tweezer.config.config import Configor
from tweezer.core.cert_installer import CertInstaller
from tweezer.model.device_type import DeviceType
from tweezer.model.exec_env import ExecEnv
from tweezer.model.traffic_type import TrafficType
from tweezer.resource import constant, resource
from tweezer.resource.resource import PackageResource, CwdResource
from tweezer.resource.runtime import Runtime
from tweezer.util.wrapper import exit_tweezer
from wisbec import system, path
from wisbec.android.adb import Adb
from wisbec.console import shell
from wisbec.console.shell import exec_cmd
from wisbec.design_patterns.singleton import SingletonType
from wisbec.file.zip import ZipUtil
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log


class Init(metaclass=SingletonType):
    def __init__(self):
        self.m_device_id = ''

    @staticmethod
    def is_adb_tool_installed() -> bool:
        code, output, err = shell.exec_cmd(['adb', 'version'])
        if code != 0:
            return False
        else:
            return True

    @staticmethod
    def install_adb_tool() -> bool:
        adb_tool_zip_path = PackageResource.get_adb_tool_path()
        if not FilesystemUtil.is_file_exist(adb_tool_zip_path):
            Log.error('adb安装文件不存在')
            return False
        extracted_adb_tool_path = os.path.join(PackageResource.get_installation_pkg_path(), 'adb_tool')
        Log.info('正在安装adb到{}...', extracted_adb_tool_path)
        FilesystemUtil.create_directories(extracted_adb_tool_path)
        if system.is_windows():
            adb_name = 'adb.exe'
        else:
            adb_name = 'adb'
        adb_path = os.path.join(extracted_adb_tool_path, 'platform-tools', adb_name)
        Log.info('正在安装adb...')
        if not FilesystemUtil.is_file_exist(adb_path):
            ZipUtil.unzip_file(adb_tool_zip_path, extracted_adb_tool_path)
            Log.info('检查是否安装成功...')
            if not FilesystemUtil.is_file_exist(adb_path):
                Log.error('adb安装失败，请尝试手动安装')
                return False
        if not system.is_windows():
            Log.info('正在给adb添加执行权限...')
            FilesystemUtil.add_executable(adb_path)
        Adb.init(adb_path)
        return True

    def init_adb(self):
        if not self.is_adb_tool_installed():
            if not self.install_adb_tool():
                Log.error('初始化adb失败')
                exit_tweezer()

    def choose_proxy_device(self):
        device_id_list = Adb.devices(True)
        if not device_id_list:
            Log.info('请插入adb设备！')
            exit_tweezer()

        if len(device_id_list) == 1:
            Log.info('默认选取adb工作设备： {}', device_id_list[0])
            self.m_device_id = device_id_list[0]
            Adb.set_device_id(self.m_device_id)
        else:
            msg = '请选择工作设备： {0}'.format(os.linesep)
            for i in range(len(device_id_list)):
                msg += '{0}\t{1}{2}'.format(i + 1, device_id_list[i], os.linesep)
            Log.info(msg)
            while True:
                index = int(input("选择工作设备id:")) - 1
                if (0 > index) or (index >= len(device_id_list)):
                    Log.error('id输入错误')
                else:
                    Log.info('已选取adb工作设备:{}', device_id_list[index])
                    self.m_device_id = device_id_list[index]
                    Adb.set_device_id(self.m_device_id)
                    break

    def __check_device_is_rooted(self) -> bool:
        # for su_path in constant.SU_PATHS:
        #     code, out, err = Adb.shell(self.m_device_id, 'ls', su_path)
        #     if 'No such file or director' not in out:
        #         return True
        # return False
        return Adb.is_rooted(self.m_device_id)

    def __install_certificate(self):
        try:
            cacert_path = os.path.join(path.home_dir(), '.mitmproxy', constant.CACERTS_NAME)
            print("cacert_path :" + cacert_path)
            if os.path.exists(cacert_path) is False:
                is_suc, mitmdump_path = self.get_mitmdump_path()
                if not is_suc:
                    raise Exception('未找到mitmdump')
                # DO NOT DELETE! This code is used to generate mitm certificate
                # on mitmproxy newly installed machine
                exec_cmd([mitmdump_path, '-p', '99999'])
            # cert_installer = CertInstaller(self.m_device_id, cacert_path)
            # if cert_installer.is_installed() is False:
            #     Log.warning('CA证书还未安装, 进行安装...')
            #     cert_installer.install()
            #     Log.info('CA证书安装成功！')
        except Exception as e:
            Log.error('证书安装失败, 原因:{}', str(e))
            exit_tweezer()

    def __set_auto_screen_lock_interval(self):
        minutes = 30
        Adb.shell(self.m_device_id, 'settings', 'put', 'system', 'screen_off_timeout', str(minutes * 60 * 1000))
        Log.info('将自动锁屏时间设定为{}分钟.', minutes)

    def init_device(self):
        # choose device
        self.choose_proxy_device()
        Runtime().device_id = self.m_device_id
        # check root
        # is_rooted = self.__check_device_is_rooted()
        
        # if not is_rooted:
        #     Log.error('{} 设备未被ROOT, 无法对指定APP抓包！', self.m_device_id)
        #     exit_tweezer()
        # check certificate
        self.__install_certificate()
        # extend time to inactivity
        self.__set_auto_screen_lock_interval()

    @staticmethod
    def init_output_dir():
        FilesystemUtil.create_directories(CwdResource.get_output_path())

    def init_exec_dev_info(self):
        sdk_level = Adb.get_sdk_level(self.m_device_id)
        dev_model = Adb.get_device_model(self.m_device_id)
        exec_env = ExecEnv(dev_model, sdk_level, TrafficType.WIFI, '上海', '上海浦东新区')
        Runtime().exec_env = exec_env

    @staticmethod
    def init_jsonpickle():
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)

    @staticmethod
    def init_config():
        resource.copy_resources_to_cwd()
        FilesystemUtil.iter_file_op(CwdResource.get_tweezer_path(), FilesystemUtil.make_user_rw)
        Configor.load_config()

    @staticmethod
    def init_log():
        log_level_str = Configor.get_tweezer_conf()['log_level']
        log_level_dict = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        Log.init_logger(log_dir=CwdResource.get_log_path(), console_log_level=log_level_dict[log_level_str])

    @staticmethod
    def get_mitmdump_path() -> (bool, str):
        if system.is_windows():
            which_executable = 'where'
        else:
            which_executable = 'which'
        code, mitmdump_path, err = shell.exec_cmd([which_executable, 'mitmdump'])
        if code != 0:
            return False, ''
        else:
            return True, str(mitmdump_path).rstrip()

    @staticmethod
    def install_mitmproxy() -> bool:
        code, output, err = shell.exec_cmd(['pip3', 'install', PackageResource.get_mitmproxy_wheel_pkg_path()])
        if code != 0:
            print('install mitmproxy failed:', err)
            return False
        return True

    def init_mitm(self) -> str:
        is_suc, mitmdump_path = self.get_mitmdump_path()
        if not is_suc:
            print('mitmproxy not installed,try to install...')
            is_suc = self.install_mitmproxy()
            if not is_suc:
                return ''
            is_suc, mitmdump_path = self.get_mitmdump_path()
            if not is_suc:
                return ''
        else:
            print('mitmdump path:', mitmdump_path)
            return mitmdump_path
