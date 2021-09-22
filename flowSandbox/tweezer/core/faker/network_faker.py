# coding=utf-8

import traceback

from tweezer.core.frida_hooker import FridaHooker
from tweezer.model.wifi import WifiInfo
from wisbec.logging.log import Log


class NetworkFaker:
    TYPE_4G = 0
    TYPE_WIFI = 1
    s_instances = {}  # {dev_id: obj}
    m_frida_hooker: FridaHooker = None

    def __init__(self, dev_id):
        caller = traceback.extract_stack()[-2][2]
        assert caller == 'instance', "Please use {}.instance() got it.".format(NetworkFaker.__name__)
        self.m_frida_hooker = FridaHooker.instance(dev_id)
        pass

    @staticmethod
    def instance(device_id):
        # 每个adb 1个单例
        if device_id not in NetworkFaker.s_instances:
            NetworkFaker.s_instances[device_id] = NetworkFaker(device_id)
        return NetworkFaker.s_instances[device_id]

    @staticmethod
    def gen_mobile_js():
        js_code = """
        Java.perform(function () {
        
            var $ = new JavaHelper(); 
        
            /////////////////////////// 网络类型： mobile network ///////////////////////////
            $.hookMethod("android.net.NetworkInfo", "getType", [], function(obj, args) {
                send("on getType()");
                // var retval = this.apply(obj, args);
                return 0; // TYPE_MOBILE: 0   TYPE_WIFI: 1
        
            });
            $.hookMethod("android.net.NetworkInfo", "getSubtype", [], function(obj, args) {
                send("on getSubtype()");
                // var retval = this.apply(obj, args);
                return 13;   // NETWORK_TYPE_LTE: 13    / WIFI: NETWORK_TYPE_UNKNOWN : 0
            });
        
            $.hookMethod("android.net.NetworkInfo", "getTypeName", [], function(obj, args) {
                send("on getTypeName()");
          
                return "MOBILE";  // WIFI: 'WIFI' 
            });
        
            $.hookMethod("android.net.NetworkInfo", "getSubtypeName", [], function(obj, args) {
                send("on getSubtypeName()");
          
                return "LTE";   // WIFI: ''
            });
        }); 
        """
        return js_code

    @staticmethod
    def __ip2dword(ip):
        tmp = ip.split('.')
        ip_dword = (int(tmp[3]) << 24) + (int(tmp[2]) << 16) + (int(tmp[1]) << 8) + int(tmp[0])
        return ip_dword

    @staticmethod
    def gen_wifi_js(ssid, bssid, mac, ip):
        ip_dword = NetworkFaker.__ip2dword(ip)

        js_code = """
        Java.perform(function () {
        
            var $ = new JavaHelper(); 
            
            
            /////////////////////////// WIFI信息 ///////////////////////////
            $.hookMethod("android.net.wifi.WifiManager", "isWifiEnabled", [], function(obj, args) {
                send("on isWifiEnabled()");
          
                return true; // true
            });
        
            $.hookMethod("android.net.wifi.WifiManager", "getWifiState", [], function(obj, args) {
                send("on getWifiState()");
          
                return 3;   // WIFI_STATE_ENABLING
            });
        
            $.hookMethod("android.net.wifi.WifiManager", "getDhcpInfo", [], function(obj, args) {
                send("on getDhcpInfo()");
                var dhcpinfo = this.apply(obj, args);
                dhcpinfo.ipAddress.value = ${ip_dword};
                dhcpinfo.netmask.value = ${netmask};
                dhcpinfo.gateway.value = ${gateway};
                dhcpinfo.serverAddress.value = ${ip_dword};
                dhcpinfo.dns1.value = ${ip_dword};
                // dhcpinfo.dns2.value = ${dns2};
                return dhcpinfo;
            });
        
        
            $.hookMethod("android.net.wifi.WifiInfo", "getNetworkId", [], function(obj, args) {
                send("on getNetworkId()");
          
                return 1; 
            });
        
            $.hookMethod("android.net.wifi.WifiInfo", "getSSID", [], function(obj, args) {
                send("on getSSID()");
          
                return "${ssid}"; 
            });
        
            $.hookMethod("android.net.wifi.WifiInfo", "getBSSID", [], function(obj, args) {
                send("on getBSSID()");
          
                return "${bssid}"; 
            });
        
            $.hookMethod("android.net.wifi.WifiInfo", "getMacAddress", [], function(obj, args) {
                send("on getMacAddress()");
          
                return "${mac}"; 
            });
        
            $.hookMethod("android.net.wifi.WifiInfo", "getIpAddress", [], function(obj, args) {
                send("on getIpAddress()");
          
                return ${ip_dword};  // C0 A8 01 69 == 192.168.1.105
            });  
        
            /////////////////////////// 屏蔽周边WIFI 扫描结果 //////////////////////////////
                $.hookMethod("android.net.wifi.WifiManager", "getScanResults", [], function(obj, args) {
                send("on getScanResults()");
          
                return Java.use("java.util.ArrayList").$new();;  // 构造空结果，
            });  
        }); 
        """.replace('${ssid}', ssid) \
            .replace('${bssid}', bssid) \
            .replace('${mac}', mac) \
            .replace('${ip_dword}', str(NetworkFaker.__ip2dword(ip))) \
            .replace('${netmask}', str(NetworkFaker.__ip2dword('255.255.255.0'))) \
            .replace('${gateway}', str(NetworkFaker.__ip2dword(ip[:ip.rfind('.')] + '.1')))
        return js_code

    # 模拟为蜂窝网络
    def fake_as_mobile(self):
        js_code = NetworkFaker.gen_mobile_js()
        if self.m_frida_hooker.spawn_hook([js_code], None, True) == -1:
            Log.error("Frida hook cellular failed")

    # 模拟为wifi网络
    # ssid: 'weiqing'
    # bssid: '04:18:d6:d3:c7:b5'
    # mac: '00:B2:00:00:00:A5'
    # ip: '192.168.1.1'
    def fake_as_wifi(self, wifi_info: WifiInfo):
        js_code = NetworkFaker.gen_wifi_js(wifi_info.m_ssid, wifi_info.m_bssid, wifi_info.m_mac, wifi_info.m_ip)
        if self.m_frida_hooker.spawn_hook([js_code], None, True) == -1:
            Log.error("Frida hook wifi failed")

    def stop_fake(self):
        pass
