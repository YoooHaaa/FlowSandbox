# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : mitm_cert.py
# Time       ：12/28/20 09:40
# Author     ：Rodney Cheung
"""
import os

from tweezer.resource import constant
from tweezer.resource.resource import PackageResource
from wisbec.android.adb import Adb
from wisbec.file.file import FileUtil


class MitmCertException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class MitmCert:
    m_cacert_path = ''
    m_device_id = ''

    def __init__(self, device_id, cacert_path):
        self.m_cacert_path = cacert_path
        self.m_device_id = device_id

    def __get_cert_path_on_sdcard(self):
        sdcard_dex_path = '/sdcard/' + os.path.basename(self.m_cacert_path)
        return sdcard_dex_path

    def __get_cert_path_on_data(self, pkg):
        data_dex_path = constant.APP_DATA_PATH_TEMP_TP.format(pkg, constant.CACERTS_HASH_NAME)
        return data_dex_path

    def get_frida_script(self, target_pkg):
        script_path = PackageResource.get_frida_mitm_cert_path()
        script_code_template = FileUtil.read_file(script_path).decode()
        script_code = script_code_template.replace('${mitm_cert_hash_name}', constant.CACERTS_HASH_NAME)
        script_code = script_code.replace('${mitm_cert_path}', self.__get_cert_path_on_data(target_pkg))
        return script_code

    def install(self, target_pkg):
        dex_cert_on_sdcard = self.__get_cert_path_on_sdcard()
        dex_cert_on_data = self.__get_cert_path_on_data(target_pkg)
        if Adb.push(self.m_device_id, self.m_cacert_path, dex_cert_on_sdcard) is False:
            raise MitmCertException('上传CA证书到{}失败！'.format(dex_cert_on_sdcard))
        code, out, err = Adb.su_shell(self.m_device_id, 'cp', dex_cert_on_sdcard, dex_cert_on_data)
        if (out+err).strip() != '':
            raise MitmCertException('拷贝证书到{}失败！'.format(dex_cert_on_data))
        code, out, err = Adb.su_shell(self.m_device_id, 'chmod', '777', dex_cert_on_data)
        if (out + err).strip() != '':
            raise MitmCertException('修改读写属性{}失败！'.format(dex_cert_on_data))