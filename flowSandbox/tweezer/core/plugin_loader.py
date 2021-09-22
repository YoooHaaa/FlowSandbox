# coding=utf-8

import importlib
import os
import threading

from tweezer.util.log import LogUtil
from wisbec.filesystem.filesystem import FilesystemUtil
from wisbec.logging.log import Log

from tweezer.config.config import Configor
from tweezer.plugins.base.base_ad_plugin import BaseAdPlugin
from tweezer.plugins.base.base_hotkey_plugin import BaseHotkeyPlugin
from tweezer.plugins.base.base_plugin import BasePlugin


class PluginLoader:
    def __init__(self, plugins_dir: str):
        self.m_plugins_dir: str = plugins_dir

    @staticmethod
    def __load_category_plugins(category_dir: str) -> list:
        plugin_file_list = FilesystemUtil.list_dir(category_dir, include_ext_name='.py')
        plugin_class_list = []
        plugin_category = os.path.basename(category_dir)
        if plugin_category == 'base' or plugin_category == '__pycache__' or plugin_category == 'ad':
            return plugin_class_list
        plugin_load_options = Configor.get_tweezer_conf()['plugins'][plugin_category]
        if not plugin_load_options['enabled']:
            return plugin_class_list
        for plugin_file in plugin_file_list:
            module_file = os.path.basename(plugin_file)
            module_name = module_file[:-3]
            if module_file == '__init__.py':
                continue
            if not plugin_load_options[module_name]['enabled']:
                Log.info('{}插件不加载', module_name)
                continue
            # load module
            class_name = plugin_load_options[module_name]['name']
            module = importlib.import_module('tweezer.plugins.{0}.{1}'.format(plugin_category, module_name))
            try:
                plugin_class = getattr(module, class_name)
            except Exception as e:
                Log.error("插件加载失败, 请检查: {}".format(module_name))
                continue
            # check super class
            if BasePlugin in plugin_class.__bases__:
                pass
            elif BaseHotkeyPlugin in plugin_class.__bases__:
                pass
            elif BaseAdPlugin in plugin_class.__bases__:
                pass
            else:
                Log.error("无效的插件, 该插件未继承: {0}、{1}或者{2}".format(BasePlugin.__name__,
                                                               BaseHotkeyPlugin.__name__, BaseAdPlugin.__name__))
                continue
            plugin_class_list.append(plugin_class)
        return plugin_class_list

    def __load_plugins(self) -> list:
        plugin_class_list = []
        plugin_cate_dir_list = FilesystemUtil.list_dirs_on_dir(self.m_plugins_dir)
        for plugin_cate_dir in plugin_cate_dir_list:
            plugin_class_list.extend(self.__load_category_plugins(plugin_cate_dir))
        return plugin_class_list

    @staticmethod
    def __start_plugin(clazz):
        plugin_obj = clazz()
        try:
            threading.Thread(target=plugin_obj.run).start()
            Log.info("加载插件成功： {}", clazz.__name__)
        except Exception as e:
            Log.critical("加载{0}插件失败", clazz.__name__)
            LogUtil.critical_exception(e)
        pass

    def start_all(self):
        list_classes = self.__load_plugins()
        for clazz in list_classes:
            self.__start_plugin(clazz)
