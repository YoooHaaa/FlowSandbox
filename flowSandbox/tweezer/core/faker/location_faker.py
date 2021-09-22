# coding=utf-8

import json
import traceback

from tweezer.resource.resource import PackageResource
from wisbec.android.adb import Adb
from wisbec.logging.log import Log


class LocationFaker:
    OP_MOCK_LOCATION = 58  # AppOpsManager.java

    s_instances = {}  # {dev_id: obj}
    s_dict_geoinfo = None
    s_mock_apk_path = PackageResource.get_mock_location_apk_path()
    s_mock_app_pkg = 'com.pkiller.mocklocation'
    m_dev_id = None

    def __init__(self, dev_id):
        caller = traceback.extract_stack()[-2][2]
        assert caller == 'instance', "Please use {}.instance() got it.".format(LocationFaker.__name__)
        self.m_dev_id = dev_id
        LocationFaker.s_dict_geoinfo = LocationFaker.__load_geoinfo()

    @staticmethod
    def instance(device_id: str):
        # 每个adb 1个单例
        if device_id not in LocationFaker.s_instances:
            LocationFaker.s_instances[device_id] = LocationFaker(device_id)
        return LocationFaker.s_instances[device_id]

    # area: 仅用于显示标识, 对模拟效果无影响
    def start_fake(self, area, latitude, longitude):
        if not Adb.is_installed(self.m_dev_id, LocationFaker.s_mock_app_pkg):
            Log.info('位置伪装app未安装，开始安装...')
            if self.__install_mock_app(LocationFaker.s_mock_apk_path) is False:
                return False
        if self.__grant_all_permission(LocationFaker.s_mock_app_pkg) is False:
            return False
        if not self.stop_fake():
            return False
        return self.__start_mock_location(area, longitude, latitude)

    def stop_fake(self) -> bool:
        return self.__stop_mock_location()

    def __start_mock_location(self, area, longitude, latitude):
        is_suc, err_reason = Adb.start_service(self.m_dev_id, '-n', 'com.pkiller.mocklocation/.MockLocationService',
                                               '--es', 'area', area, '--ef', 'latitude', str(latitude), '--ef',
                                               'longitude', str(longitude))
        if not is_suc:
            Log.error('start mock location failed:{}', err_reason)
        return is_suc

    def __stop_mock_location(self):
        is_suc, err_reason = Adb.stop_service_s(self.m_dev_id, '-n', 'com.pkiller.mocklocation/.MockLocationService')
        if not is_suc:
            Log.error('stop mock location failed:{}', err_reason)
        return is_suc

    # return: {'province': {'city': (latitude, longitude), ...} , }
    @staticmethod
    def __load_geoinfo():
        geoinfo_dict = {}
        # https://github.com/rkern/line_profiler/issues/37#issuecomment-153312587
        with open(PackageResource.get_geoinfo_china_path(), 'rb') as f:
            def center_2_coordinate(center):
                latitude_str, longitude_str = center.split(',')
                return float(latitude_str), float(longitude_str)

            province_list = json.load(f)
            for province_dict in province_list:
                province_name = province_dict['name']
                city_list = province_dict['districts']

                geoinfo_dict[province_name] = {}
                for city_dict in city_list:
                    city_name = city_dict['name']
                    latitude, longitude = center_2_coordinate(city_dict['center'])
                    geoinfo_dict[province_name][city_name] = (latitude, longitude)
        return geoinfo_dict

    def __install_mock_app(self, apk_path):
        if Adb.install(self.m_dev_id, apk_path) is False:
            Log.error("Failed to install mock location app.")
            return False
        return True

    def __grant_all_permission(self, pkg_name):
        dict_permissions = Adb.get_app_permission(self.m_dev_id, pkg_name)
        if dict_permissions is None:
            Log.error('Failed to get permissions of mock location app.')
            return False
        for name, mode in dict_permissions.items():
            if mode == 'allow':
                continue
            if name == 'android.permission.ACCESS_MOCK_LOCATION':
                if self.__enable_mock_app() is False:
                    Log.error('Failed to activate mock location app.')
                    return False
            else:
                is_suc, err_reason = Adb.grant_permission(self.m_dev_id, pkg_name, name)
                if is_suc is False and 'Unknown permission' not in err_reason:
                    Log.error('Failed to grant permissions for mock location app:{}', err_reason)
                    return False
        return True

    def __enable_mock_app(self):
        return Adb.appops_set(self.m_dev_id, LocationFaker.s_mock_app_pkg, LocationFaker.OP_MOCK_LOCATION, 'allow')

    def __disable_mock_app(self):
        return Adb.appops_set(self.m_dev_id, LocationFaker.s_mock_app_pkg, LocationFaker.OP_MOCK_LOCATION, 'default')

    @staticmethod
    def get_provinces():
        if LocationFaker.s_dict_geoinfo is None:
            LocationFaker.s_dict_geoinfo = LocationFaker.__load_geoinfo()

        return list(LocationFaker.s_dict_geoinfo.keys())

    @staticmethod
    def get_cities(province):
        if LocationFaker.s_dict_geoinfo is None:
            LocationFaker.s_dict_geoinfo = LocationFaker.__load_geoinfo()

        if province not in LocationFaker.s_dict_geoinfo:
            return None

        return list(LocationFaker.s_dict_geoinfo[province].keys())

    # return: longitude, latitude
    @staticmethod
    def area_2_coordinates(province, city):
        if LocationFaker.s_dict_geoinfo is None:
            LocationFaker.s_dict_geoinfo = LocationFaker.__load_geoinfo()
        return LocationFaker.s_dict_geoinfo[province][city]
