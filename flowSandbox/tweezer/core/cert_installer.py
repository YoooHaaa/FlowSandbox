# coding=utf-8

import os

from wisbec.android.adb import Adb
from wisbec.crypto.hash import HashUtil
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log

from tweezer.resource import constant


class CertInstallerException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class CertInstaller:
    m_cacert_path = ''
    m_device_id = ''

    def __init__(self, device_id, cacert_path):
        self.m_cacert_path = cacert_path
        self.m_device_id = device_id

    def is_path_exists(self, path):
        code, out, err = Adb.shell(self.m_device_id, 'ls', path)
        return 'No such file or director' not in out + err

    def is_installed(self):
        remote_cacert_path = constant.CACERTS_ADDED_DIR + '/' + constant.CACERTS_HASH_NAME
        remote_cacert_exist = self.is_path_exists(remote_cacert_path)
        if not remote_cacert_exist:
            return False
        remote_cacert_tmp_save_path = os.path.join(os.getcwd(), constant.CACERTS_HASH_NAME)
        if not Adb.pull(self.m_device_id, remote_cacert_path, remote_cacert_tmp_save_path):
            return False
        local_cert_md5 = HashUtil.get_file_md5(self.m_cacert_path)
        remote_cert_md5 = HashUtil.get_file_md5(remote_cacert_tmp_save_path)
        FilesystemUtil.remove(remote_cacert_tmp_save_path)
        return local_cert_md5 == remote_cert_md5

    def install(self):
        # code, out, err = Adb.su_shell(self.m_device_id, 'id')
        # if '(root)' not in out:
        if not Adb.is_rooted(self.m_device_id):
            raise CertInstallerException('未获取到ROOT权限！')
        tmp_path_on_dev = '/sdcard/' + constant.CACERTS_HASH_NAME
        if Adb.push(self.m_device_id, self.m_cacert_path, tmp_path_on_dev) is False:
            raise CertInstallerException('上传CA证书失败！')

        if not Adb.is_system_partition_rw(self.m_device_id):
            code, out, err = Adb.su_shell(self.m_device_id, 'mount', '-o', 'remount,rw', '/system')
            code2, out2, err2 = Adb.su_shell(self.m_device_id, 'mount', '-o', 'rw,remount', '/system')
            if out + err != '' and out2 + err2 != '':
                Log.info('重新挂载/system为可写失败,尝试重新挂载/')
                code, out, err = Adb.su_shell(self.m_device_id, 'mount', '-o', 'remount,rw', '/')
                code2, out2, err2 = Adb.su_shell(self.m_device_id, 'mount', '-o', 'rw,remount', '/')
                if out + err != '' and out2 + err2 != '':
                    raise CertInstallerException('重新挂载/为可写失败！')
                else:
                    Log.info('挂载/成功!')

        #     if out+err != '':
        #
        #     # disable-verify
        #     Log.warning("当前设备可能开启了dm-verity, 尝试禁用中, 请稍等...")
        #     is_succ, err = Adb.disable_verify(self.m_device_id)
        #     if is_succ is False:
        #         raise CertInstallerException('禁用dm-verify失败： {}'.format(err))
        #     Log.warning("禁用dm-verify完毕, 正在重启设备, 请稍等...")
        #     code, out, err = Adb.exec('-s', self.m_device_id, "reboot")
        #     time.sleep(2)
        #     if Adb.wait_device(self.m_device_id, 5*60) is False:
        #         raise CertInstallerException('等待设备重新启动超时')
        #     Log.warning("设备重新启动成功，重新尝试安装证书...")
        #     self.install()
        # if out+err != '':
        #     raise CertInstallerException('重新挂载/system为可写失败！')

        code, out, err = Adb.su_shell(self.m_device_id, 'cp', tmp_path_on_dev, constant.CACERTS_ADDED_DIR)
        if out != '':
            raise CertInstallerException('拷贝文件到{}失败！'.format(constant.CACERTS_ADDED_DIR))

        certs_path_on_device = constant.CACERTS_ADDED_DIR + '/' + constant.CACERTS_HASH_NAME
        code, out, err = Adb.su_shell(self.m_device_id, 'chmod', '644', certs_path_on_device)
        if out != '':
            raise CertInstallerException('修改读写属性{}失败！'.format(certs_path_on_device))

        return self.is_installed()

    pass
