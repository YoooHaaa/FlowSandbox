# coding=utf-8
# 该模块必须结合frida脚本： resource/persist/frida_core/http_proxy.js一同使用才会生效。
# 该模块向系统设置相关property项, 以便让http_proxy.js脚本获取正确的 pkg, host, port参数。

import traceback

from tweezer.resource.resource import PackageResource
from wisbec.android.adb import Adb
from wisbec.file.file import FileUtil


class HttpProxy:
    s_instances = {}
    m_script_code = None
    m_task_id = -1

    def __init__(self, device_id):
        caller = traceback.extract_stack()[-2][2]
        assert caller == 'instance', "Please use {}.instance() got it.".format(HttpProxy.__name__)

        self.m_device_id = device_id

        with open(PackageResource.get_frida_http_proxy_path(), "rb") as fd:
            self.m_script_code = fd.read().decode('utf-8')

    @staticmethod
    def instance(device_id):
        # 每个adb 1个单例
        if device_id not in HttpProxy.s_instances:
            HttpProxy.s_instances[device_id] = HttpProxy(device_id)

        return HttpProxy.s_instances[device_id]

    @staticmethod
    def get_frida_script():
        script_path = PackageResource.get_frida_http_proxy_path()
        script_code = FileUtil.read_file(script_path).decode()
        return script_code

    def start_proxy(self, pkg, host, port):
        Adb.set_prop(self.m_device_id, 'sandbox.httpproxy.packagename', pkg)
        Adb.set_prop(self.m_device_id, 'sandbox.httpproxy.host', host)
        Adb.set_prop(self.m_device_id, 'sandbox.httpproxy.port', str(port))


    def stop_proxy(self):
        Adb.set_prop(self.m_device_id, 'sandbox.httpproxy.packagename', '')
