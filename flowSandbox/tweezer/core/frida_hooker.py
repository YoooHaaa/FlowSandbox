# coding=utf-8

import copy
import os
import re
import threading
import time
import traceback
from typing import List

import frida

from tweezer.resource.resource import PackageResource
from wisbec.android.adb import Adb
from wisbec.logging.log import Log
from wisbec.shell_parser.model.ps_info import PsInfo
from wisbec.shell_parser.ps import PsParser


class BaseHelper:
    m_device_id = None
    m_server_host_path = None
    m_server_dev_path = None
    m_frida_device = None

    def __init__(self, device_id):
        self.m_device_id = device_id
        self.m_frida_device = self.get_device(device_id)
        dev_abi = Adb.get_prop(device_id, 'ro.product.cpu.abi')
        if 'arm64' in dev_abi:
            self.m_server_host_path = PackageResource.get_frida_server_arm64_path()
        else:
            self.m_server_host_path = PackageResource.get_frida_server_arm_path()

        self.m_server_dev_path = "/data/local/tmp/" + os.path.basename(self.m_server_host_path)

    @staticmethod
    def get_device(device_id):
        try:
            frida_device = frida.get_device(device_id)
        except frida.InvalidArgumentError as e:
            Log.error('get frida device failed:{},Try using frida.get_usb_device(1)...', str(e))
            frida_device = frida.get_usb_device(1)
        return frida_device

    def start_server(self) -> bool:
        if self.is_running():
            Adb.forward(self.m_device_id, "tcp:27042", "tcp:27042")
            Adb.forward(self.m_device_id, "tcp:27043", "tcp:27043")
            # Log.info("Frida server is running ...")
            return True
        elif self.__start_server():
            Adb.forward(self.m_device_id, "tcp:27042", "tcp:27042")
            Adb.forward(self.m_device_id, "tcp:27043", "tcp:27043")
            # Log.info("Frida server is running ...")
            return True
        else:
            # Log.info("Frida server failed to run ...")
            return False

    def __start_server(self) -> bool:
        print("Start frida server ...")

        if not Adb.is_path_exists(self.m_device_id, self.m_server_dev_path):
            if not Adb.push(self.m_device_id, self.m_server_host_path, self.m_server_dev_path):
                return False

        code, out, err = Adb.shell(self.m_device_id, "chmod", '777', self.m_server_dev_path)
        if out != '':
            return False

        threading.Thread(target=lambda: Adb.su_shell(self.m_device_id, self.m_server_dev_path)).start()
        time.sleep(1)
        return self.is_running()

    def kill_server(self) -> bool:
        # Log.debug("*", "Kill frida server ...")
        server_ps = os.path.basename(self.m_server_dev_path).replace('.', '\.')
        matched_process_list = self.get_process_by_name(server_ps)
        if len(matched_process_list) == 0:
            return True
        code, out, err = Adb.su_shell(self.m_device_id, 'kill', '-9', matched_process_list[0].pid)
        return code == 0 and out == ''

    # return : [{user: xx, pid: xx, ppid: xx, status: xx, name: xx}]
    def get_process_by_name(self, name_pattern) -> List[PsInfo]:
        matched_process_list = []
        for ps_info in self.get_processes():
            name = ps_info.name
            if re.match(name_pattern, name) is not None:
                matched_process_list.append(ps_info)
        return matched_process_list

    # return : [{user: xx, pid: xx, ppid: xx, status: xx, name: xx}]
    def get_processes(self):
        code, res1, err = Adb.su_shell(self.m_device_id, 'ps -A')
        code, res2, err = Adb.su_shell(self.m_device_id, 'ps')
        res = res1 if len(res1) > len(res2) else res2
        return PsParser.get_process(res)
        # list_matche = []
        # for line in res.strip().replace('\r\n', '\n').split('\n')[1:]:
        #     while line.find('  ') != -1:
        #         line = line.replace('  ', ' ')
        #     line = line.replace(' ', '\t')
        #     s = line.split('\t')
        #     if len(s) == 9:
        #         list_matche.append({
        #             'user': s[0],
        #             'pid': int(s[1]),
        #             'ppid': int(s[2]),
        #             'status': s[7],  # S, D, R
        #             'name': s[8]})
        #     else:
        #         Log.warning('err ps line:{}', line)
        # return list_matche

    def is_running(self) -> bool:
        server_ps = ".*" + os.path.basename(self.m_server_dev_path).replace('.', '\.') + ".*"
        matched_process_list = self.get_process_by_name(server_ps)
        return len(matched_process_list) > 0


class FridaHooker(BaseHelper):
    s_instances = {}  # {dev_id: obj}
    m_list_task = {}
    m_device_id = None
    m_pre_script_code = None
    m_lock = None

    RET_FAILED = -1
    RET_NOT_READY = 0
    """
    {'pkg':
        {
        'scripts': { 'pid0': [pid0_script_obj, pid0_script2_obj], ... },
        'sessions': {pid0: session_obj, }
        },
    }
    """
    m_dict_hooks_info = {}

    """
     {pkg: {task_id: [js_code1],} }
     }
     """
    m_dict_trace_tasks = {}  # 需要持续对新进程hook的脚本：

    """
    {task_id: [pid0_script1_obj, pid0_script2_obj, pid2_script1_obj], }
    """
    m_dict_tasks = {}

    """
     {pkg: {task_id: callback, }
     }
    """
    m_dict_tasks_cb = {}

    m_next_tasks_id = 1

    m_hooking_pid = 0
    m_hooking_pkg = None
    m_hooking_session = None

    def __init__(self, device_id):
        caller = traceback.extract_stack()[-2][2]
        assert caller == 'instance', "Please use {}.instance() got it.".format(FridaHooker.__name__)

        super().__init__(device_id)
        self.m_device_id = device_id
        self.m_lock = threading.Lock()
        with open(PackageResource.get_frida_base_path(), "rb") as fd:
            self.m_pre_script_code = fd.read().decode('utf-8')

    @staticmethod
    def instance(device_id):
        # 每个adb 1个单例
        if device_id not in FridaHooker.s_instances:
            FridaHooker.s_instances[device_id] = FridaHooker(device_id)

        return FridaHooker.s_instances[device_id]

    def __add_hook_info(self, pkg):
        if pkg not in self.m_dict_hooks_info:
            self.m_dict_hooks_info[pkg] = {'scripts': {},
                                           'sessions': {},
                                           }

    # 进程被附加
    def on_process_attached(self, session, pkg, pid):
        self.m_lock.acquire()
        if pkg not in self.m_dict_hooks_info:
            self.__add_hook_info(pkg)

        self.m_dict_hooks_info[pkg]['sessions'][pid] = session
        self.m_dict_hooks_info[pkg]['scripts'][pid] = []
        self.m_lock.release()

    def on_process_detached(self, reason, **kwargs):
        self.m_lock.acquire()
        pkg = kwargs['pkg']
        pid = kwargs['pid']
        del self.m_dict_hooks_info[pkg]['sessions'][pid]
        del self.m_dict_hooks_info[pkg]['scripts'][pid]
        self.m_lock.release()

    # 脚本加载回调
    def on_script_loaded(self, **kwargs):
        self.m_lock.acquire()
        pkg = kwargs['pkg']
        pid = kwargs['pid']
        script = kwargs['script']
        task_id = kwargs['task_id']
        self.m_dict_hooks_info[pkg]['scripts'][pid].append(script)
        if task_id not in self.m_dict_tasks:
            self.m_dict_tasks[task_id] = []
        self.m_dict_tasks[task_id].append(script)
        self.m_lock.release()

    # 脚本释放回调
    def on_script_destroyed(self, reason, **kwargs):
        print("on_script_destroyed")
        self.m_lock.acquire()
        pkg = kwargs['pkg']
        pid = kwargs['pid']
        script = kwargs['script']
        task_id = kwargs['task_id']

        list_scripts_by_process = self.m_dict_hooks_info[pkg]['scripts'][pid]
        try:
            i = list_scripts_by_process.index(script)
            del list_scripts_by_process[i]
        except Exception as e:
            pass

        list_scripts_by_task = self.m_dict_tasks[task_id]
        try:
            i = list_scripts_by_task.index(script)
            del list_scripts_by_task[i]
        except Exception as e:
            pass
        self.m_lock.release()

    def on_script_message(self, message, data, **kwargs):
        task_id = kwargs['task_id']
        if task_id in self.m_dict_tasks_cb:
            self.m_dict_tasks_cb[task_id](message)

        # if message['type'] == 'send':
        #     print("[*] {0}".format(message['payload']))
        # else:
        #     print(message)

    def on_device_spawn_added(self, spawn):
        print("on_device_spawn_added")
        process_name = spawn.identifier
        pkg = self.__get_hooking_pkg_with_processname(process_name)
        if pkg is None:
            # 不属于当前正在hook的应用
            try:
                self.m_frida_device.resume(spawn.pid)
                Log.info("ignored process: {} - {}", spawn.identifier, spawn.pid)
            except frida.InvalidArgumentError as e:
                Log.warning(" invalied PID: {}, {}", spawn.pid, process_name)
            return
        Log.info("caught process, inject it: {} - {}", spawn.identifier, spawn.pid)
        self.__hook_new_process(pkg, spawn.pid, process_name)

    def on_device_spawn_removed(self, reason):
        pass

    def on_device_child_added(self, reason):
        pass

    def on_device_child_removed(self, reason):
        pass

    def on_device_process_crashed(self, reason):
        pass

    def on_device_uninjected(self, reason):
        pass

    def on_device_lost(self, reason):
        pass

    def on_device_output(self, reason):
        pass

    def __start_server(self):
        if self.is_running() is False and self.start_server():
            self.__init_device_callback(self.m_frida_device)
            return True
        elif self.is_running():
            self.__init_device_callback(self.m_frida_device)
            return True
        return False

    def __stop_server(self):
        return self.kill_server()

    def __init_device_callback(self, device: frida.core.Device):
        device.on('spawn-added', self.on_device_spawn_added)  # 孵化新进程被捕获： on_device_spawn_added() 被调用
        device.on('spawn-removed', self.on_device_spawn_removed)  # 孵化新进程被释放： on_device_spawn_removed() 被调用
        device.on('child-added', self.on_device_child_added)  # 同上，fork ?
        device.on('child-removed', self.on_device_child_removed)  # 同上，fork ?
        device.on('process-crashed', self.on_device_process_crashed)  # 进程崩溃
        device.on('uninjected', self.on_device_uninjected)  # 暂不清楚触发时机
        device.on('lost', self.on_device_lost)  # 连接丢失时被触发，如：usb线断掉，adb中断。
        device.on('output', self.on_device_output)
        device.enable_spawn_gating()  # 监控zygote进程spawn新进程, 启用后spawn-added、spawn-removed才会被回调

    def __init_session_callback(self, session: frida.core.Session, pkg, pid):
        kwargs = {
            "pkg": pkg,
            "pid": pid,
            "session": session,
        }

        # 1. 主动调用session.detach()时
        # 2. 进程被杀掉时
        # 3. usb连接断掉、adb中断时
        # 4. 进程崩溃时
        session.on('detached', lambda reason: self.on_process_detached(reason, **kwargs))

        # 启用child_gating后，有些应用会卡死或崩溃(不加载任何frida脚本的情况下)。 如： vivo视频。
        # session.enable_child_gating() # 监控进程中fork出的新进程或死掉的子进程进行拦截, 启用后child-added、child-removed才会被回调。

    def __init_script_callback(self, script: frida.core.Script, pkg, pid, task_id):
        kwargs = {
            "pkg": pkg,
            "pid": pid,
            "task_id": task_id,
            "script": script
        }
        script.on('message', lambda message, data: self.on_script_message(message, data, **kwargs))

        # 1. 主动调用session.detach()时，或主动调用script.unload()时。
        # 2. 进程被杀掉时
        # 3. usb连接断掉、adb中断时
        # 4. 进程崩溃时
        script.on("destroyed", lambda reason: self.on_script_destroyed(reason, **kwargs))

    def __is_process_attached(self, pkg, pid):
        self.m_lock.acquire()
        if pkg not in self.m_dict_hooks_info:
            self.m_lock.release()
            return False

        if pid not in self.m_dict_hooks_info[pkg]['sessions']:
            self.m_lock.release()
            return False

        self.m_lock.release()
        return True

    def __get_attached_session(self, pkg, pid):
        self.m_lock.acquire()
        if pkg not in self.m_dict_hooks_info:
            self.m_lock.release()
            return None

        if pid not in self.m_dict_hooks_info[pkg]['sessions']:
            self.m_lock.release()
            return None

        session = self.m_dict_hooks_info[pkg]['sessions'][pid]
        self.m_lock.release()
        return session

    def __attach_process(self, pkg, pid):
        if self.__is_process_attached(pkg, pid) is False:
            session = None
            try:
                session = self.m_frida_device.attach(pid)
            except frida.TransportError as e:
                Log.warning("attach process {} fail: {}", pid, e)
                return None
            except Exception as e:
                traceback.print_exc()
                Log.warning("attach process {} fail: {}", pid, e)
                return None
            self.__init_session_callback(session=session, pkg=pkg, pid=pid)
            self.on_process_attached(session=session, pkg=pkg, pid=pid)
            return session
        else:
            return self.__get_attached_session(pkg, pid)

    def __allow_new_task_id(self):
        return self.m_next_tasks_id

    def __inc_next_task_id(self):
        self.m_next_tasks_id += 1

    def __get_hooking_pkgs(self):
        return list(self.m_dict_hooks_info.keys())

    def __is_app_process(self, pkg, process_name):
        if pkg == process_name:
            return pkg == process_name
        return (pkg + '.' in process_name) or (pkg + ':' in process_name) or (pkg + '@' in process_name)

    def __get_hooking_pkg_with_processname(self, process_name):
        for pkg in self.__get_hooking_pkgs():
            if self.__is_app_process(pkg, process_name):
                return pkg
        return None

    def __add_trace_script(self, pkg, list_scripts_code: list, task_id):
        if pkg not in self.m_dict_trace_tasks:
            self.m_dict_trace_tasks[pkg] = {}

        self.m_dict_trace_tasks[pkg][task_id] = list_scripts_code

    def __add_task_callback(self, task_id, callback):
        self.m_dict_tasks_cb[task_id] = callback

    # return: [(task_id, list_scripts_code), ]
    def __get_trace_tasks(self, pkg):
        if pkg not in self.m_dict_trace_tasks:
            return []
        list_tasks = []
        for k, v in self.m_dict_trace_tasks[pkg].items():
            list_tasks.append((k, v))
        return list_tasks

    # hook应用运行中，新创建的进程
    def __hook_new_process(self, pkg, pid, process_name):
        session = self.__attach_process(pkg, pid)
        if session is None:
            Log.warning("attach spawn process failed: {}, {}", pkg, process_name)
            try:
                self.m_frida_device.resume(pid)
            except Exception as e:
                pass
            return

        list_tasks = self.__get_trace_tasks(pkg)
        for task_id, list_scripts_code in list_tasks:
            for script_code in list_scripts_code:
                script = self.__run_script(session, pkg, pid, script_code, task_id)
                if script is None:
                    Log.warning("run script spawn process failed: {}, {}", pkg, process_name)
            try:
                self.m_frida_device.resume(pid)
            except Exception as e:
                pass

    def __run_script(self, session, pkg, pid, script_code, task_id):
        try:
            script = session.create_script(script_code + self.m_pre_script_code)
            kwargs = {
                "pkg": pkg,
                "session": session,
                "script": script,
                "pid": pid,
                "script_code": script_code,
                "task_id": task_id
            }
            self.__init_script_callback(script=script, pkg=pkg, pid=pid, task_id=task_id)
            script.load()
            self.on_script_loaded(**kwargs)
            return script
        except frida.TransportError as e:
            Log.warning("load script fail: {}", e)
            return None
        except Exception as e:
            traceback.print_exc()
            return None

    # return: task_id(>=0)   fail(-1)
    # callback: cb(message)
    def hook_once(self, pkg, list_scripts_code, callback=None, restart=False, trace_new_processes=False):
        self.__start_server()
        task_id = self.__allow_new_task_id()
        if not restart:
            matched_processes = self.get_process_by_name('.*' + pkg + '.*')
            if len(matched_processes) == 0:
                self.__add_hook_info(pkg)
            for process_info in self.get_process_by_name('.*' + pkg + '.*'):
                pid = process_info.pid
                session = self.__attach_process(pkg, pid)
                if session is None:
                    return FridaHooker.RET_FAILED
                for script_code in list_scripts_code:
                    script = self.__run_script(session=session, pkg=pkg, pid=pid, script_code=script_code,
                                               task_id=task_id)
                    if script is None:
                        return FridaHooker.RET_FAILED
        else:
            try:
                pid = self.m_frida_device.spawn([pkg])
                session = self.__attach_process(pkg, pid)
                if session is None:
                    return FridaHooker.RET_FAILED
                for script_code in list_scripts_code:
                    script = self.__run_script(session=session, pkg=pkg, pid=pid, script_code=script_code,
                                               task_id=task_id)
                    if script is None:
                        return FridaHooker.RET_FAILED
                self.m_frida_device.resume(pid)
            except Exception as e:
                traceback.print_exc()
                return FridaHooker.RET_FAILED

        self.__inc_next_task_id()
        if trace_new_processes:
            self.__add_trace_script(pkg, list_scripts_code, task_id)
        if callback is not None:
            self.__add_task_callback(task_id=task_id, callback=callback)
        return task_id

    # spawn_begin(), spawn_hook(), spawn_finish() 组合使用
    # return: bool
    def spawn_begin(self, pkg):
        if self.m_hooking_session is not None:
            # 当前任务进行中，需要先调用spawn_finish()
            return False
        self.__start_server()
        try:
            pid = self.m_frida_device.spawn([pkg])
            session = self.__attach_process(pkg, pid)
            if session is not None:
                self.m_hooking_pid = pid
                self.m_hooking_session = session
                self.m_hooking_pkg = pkg
                return True
            return False
        except Exception as e:
            traceback.print_exc()
            return False

    # return: task_id(>=0)   fail(-1)
    def spawn_hook(self, list_scripts_code: list, callback=None, trace_new_processes=False):
        if self.m_hooking_session is None:
            # 当前任务未开始，需要先调用spawn_begin()
            return FridaHooker.RET_NOT_READY
        task_id = self.__allow_new_task_id()
        try:
            for script_code in list_scripts_code:
                script = self.__run_script(session=self.m_hooking_session, pkg=self.m_hooking_pkg,
                                           pid=self.m_hooking_pid, script_code=script_code, task_id=task_id)
                if script is None:
                    return FridaHooker.RET_FAILED
        except Exception as e:
            traceback.print_exc()
            return FridaHooker.RET_FAILED

        self.__inc_next_task_id()
        if trace_new_processes:
            self.__add_trace_script(self.m_hooking_pkg, list_scripts_code, task_id)
        if callback is not None:
            self.__add_task_callback(task_id=task_id, callback=callback)
        return task_id

    def spawn_finish(self):
        if self.m_hooking_session is None:
            # 当前任务未开始，需要先调用spawn_begin()
            return False
        try:
            self.m_frida_device.resume(self.m_hooking_pid)
            return True
        except Exception as e:
            traceback.print_exc()
            return False
        finally:
            self.m_hooking_pid = 0
            self.m_hooking_pkg = None
            self.m_hooking_session = None

    def unhook_app(self, pkg):
        """
        {'pkg':
            {
            'scripts': { 'pid0': [pid0_script_obj, pid0_script2_obj], ... },
            'tasks': {task_id: [pid0_script_obj, pid1_script_obj]}
            'sessions': {pid0: session_obj, }
            },
        }
        """
        self.m_lock.acquire()
        if pkg not in self.m_dict_hooks_info:
            return
        dict_sessions = copy.copy(self.m_dict_hooks_info[pkg]['sessions'])
        self.m_lock.release()
        for pid, session in dict_sessions.items():
            try:
                session.detach()
            except Exception as e:
                traceback.print_exc()
                pass

    def unhook_task(self, task_id):
        self.m_lock.acquire()
        if task_id not in self.m_dict_tasks:
            self.m_lock.release()
            return
        list_task_scripts = copy.copy(self.m_dict_tasks[task_id])
        self.m_lock.release()
        for task_script in list_task_scripts:
            task_script.unload()

    def unhook_all(self):
        self.m_lock.acquire()
        dict_hooks_info = copy.copy(self.m_dict_hooks_info)
        self.m_lock.release()
        for pkg, hook_info in dict_hooks_info.items():
            for pid, session in copy.copy(hook_info['sessions']).items():
                try:
                    session.detach()
                except Exception as e:
                    traceback.print_exc()
                    pass
