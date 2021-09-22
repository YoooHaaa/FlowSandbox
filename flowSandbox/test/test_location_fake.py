# coding=utf-8

import time
from tweezer.core.faker.location_faker import LocationFaker
from wisbec.logging.log import Log
from wisbec.android.adb import Adb


Log.init_logger(is_log_to_file=False)
a = LocationFaker.instance(Adb.devices(True)[0])

provice = '内蒙古自治区'
city = a.get_cities(provice)[0]
coordinate = a.area_2_coordinates(provice, city)
a.start_fake(provice+city, coordinate[0], coordinate[1])
time.sleep(20)
a.stop_fake()
