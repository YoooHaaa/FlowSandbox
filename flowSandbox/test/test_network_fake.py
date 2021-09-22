# coding=utf-8

import time

from tweezer.model.wifi import WifiInfo

from tweezer.core.faker.network_faker import NetworkFaker
from wisbec.logging.log import Log
from wisbec.android.adb import Adb


Log.init_logger(is_log_to_file=False)
a = NetworkFaker.instance(Adb.devices(True)[0])
# NetworkFaker.instance(Adb.devices()[0]).fake_as_wifi('weiqing222', '88:88:88:88:88:88', '66:66:66:66:66:66', '192.168.8.8')
wi = WifiInfo(ip='192.168.8.8', ssid='asdfasdf', bssid='66:66:66:66:66:66', mac='88:88:88:88:88:88')
a.fake_as_wifi(pkg_name='com.geek.jk.weather', wifi_info=wi)
time.sleep(50)