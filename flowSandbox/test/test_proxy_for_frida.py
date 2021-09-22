import time

from tweezer.core.frida_hooker import FridaHooker
from wisbec.android.adb import Adb
from wisbec.logging.log import Log

Log.init_logger(is_log_to_file=False)

js_code = r"""
Java.perform(function () {

    var $ = new JavaHelper(); 

     // $.hookMethods("com.whatsapp.util.Log", "v", $.getHookImpl(false, true));
     // $.hookMethods("com.whatsapp.util.Log", "d", $.getHookImpl(false, true)); 
     // $.hookMethods("com.whatsapp.util.Log", "i", $.getHookImpl(false, true));
     // $.hookMethods("com.whatsapp.util.Log", "w", $.getHookImpl(false, true));
     // $.hookMethods("com.whatsapp.util.Log", "e", $.getHookImpl(false, true)); 
     // $.hookMethods("com.whatsapp.data.b.a", "a", $.getHookImpl(false, true)); 

    // token: 4qf/qvUY+GGYPUC2rjWCK0VX5aI=
    // $.hookMethods("com.whatsapp.registration.bt", "a", $.getHookImpl(true, true));
    // $.hookMethods("com.whatsapp.registration.bt", "a", $.getHookImpl(true, true));
    
    // [-64,46,-124,-2,33,26,96,-20,75,125,-95,-122,48,-109,61,36]
    // $.hookMethods("com.whatsapp.y.a", "b", $.getHookImpl(false, true));

    // [-44,81,-110,24,-95,-10,31,-104,62,-30,-29,-59,66,-64,126,-64]
    // $.hookMethods("d.f.X.a", "e", $.getHookImpl(false, true))

    // $.hookMethods("d.f.ga.Bb", "$init", $.getHookImpl(true, true));

    // $.hookMethods("com.whatsapp.jobqueue.job.SendE2EMessageJob", "a", $.getHookImpl(true, true));
    // $.hookClass("f.f.c.m", $.getHookImpl(true, true));

    // $.hookMethods("javax.crypto.spec.SecretKeySpec", "$init", $.getHookImpl(true, true));
    // $.hookMethods("javax.crypto.spec.IvParameterSpec", "$init", $.getHookImpl(true, true));
    // $.hookMethods("javax.crypto.Cipher", "getInstance", $.getHookImpl(true, true));
    
    // $.hookMethods("java.lang.String", "$init", $.getHookImpl(true, true));

    // com.whatsapp.tg$2
    // $.hookClass("android.app.Dialog", function(obj, args) {
    //     return this.apply(obj, args);
    // });



    // function startsWith(obj, substring) {
    //     return obj.slice(0, substring.length) === substring;
    // }

    // $.hookMethods("com.whatsapp.util.Log", "d", function(obj, args) {
    //             send('on Log.d()');
    //     send(args);
    //     if (typeof args[0] != 'string') {
    //         return;
    //     }

    //     // msgstore/addmsg/done 923362580397-1492792607@g.us BC2EA5341C51D98B75AAD17A795A55D7

    //     send(typeof args[0]);
    //     if (startsWith(args[0], 'msgstore/addmsg/done')) {
    //         var tmp = args[0].split(' ');
    //         send('msg id:' + tmp[2]);
    //         send('remote jid: ' + tmp[1]);

    //     }

    //     if (startsWith(args[0], 'computed participant hash for')) {
    //         send(args[0]);
    //     }
    // });

    // /data/data/com.whatsapp/shared_prefs/com.whatsapp_preferences.xml
    // software_forced_expiration
    // $.hookMethods("android.app.SharedPreferencesImpl", "getLong", function(obj, args) {
    //     send("on getLong()");
    //     if (args[0] == "software_forced_expiration") {
    //         return 3000000000000;
    //     }
    //     return this.apply(obj, args);
    // });


    // $.hookMethod("com.whatsapp.vj", "a", ['java.util.Collection'], function(obj, args) {
    //     send("///////////////////////////////////////////////////// on toHash()");
    //     var retval = this.apply(obj, args);
    //     send(retval);
    //     return retval; 
    // });



    // $.hookMethod("java.security.MessageDigest", "update", function(obj, args) {
    //     send("on MessageDigest.update()");
    //     send(args[0]);
    //     var retval = this.apply(this, args);
    //     return retval; 
    // });


    // $.hookMethod("com.whatsapp.w.b", "b", ['java.lang.String'], function(obj, args) {
    //     send("on bbbbbbb()");
    //     send(obj);
    //     send(args[0]);
    //     var retval = this.apply(obj, args);
    //     return retval; 
    // });




    //$.hookMethods("com.whatsapp.NewGroup$5", "$init", $.getHookImpl(false, true));


    // $.hookMethods("com.whatsapp.DialogToastActivity", "onCreate", $.getHookImpl(false, true));
    // $.hookMethods("com.whatsapp.DialogToastActivity", "onPause", $.getHookImpl(false, true));
    // $.hookMethods("com.whatsapp.DialogToastActivity", "onDestory", $.getHookImpl(false, true));
    // $.hookMethods("com.whatsapp.DialogToastActivity", "onResume", $.getHookImpl(false, true));

    // $.hookMethods("com.whatsapp.DialogToastActivity$ProgressDialogFragment", "a", $.getHookImpl(false, true));
    // $.hookMethods("com.whatsapp.DialogToastActivity$ProgressDialogFragment", "c", $.getHookImpl(false, true));
    // $.hookMethods("com.whatsapp.DialogToastActivity$ProgressDialogFragment", "e", $.getHookImpl(false, true));

    // $.hookMethods("com.whatsapp.DialogToastActivity$ProgressDialogFragment", "onDismiss", $.getHookImpl(false, true));
    // var ProgressDialogFragment = Java.use("com.whatsapp.DialogToastActivity$ProgressDialogFragment");

    // setInterval(function(){send(ProgressDialogFragment.ae);}, 1000);
    // $.hookMethod("com.whatsapp.messaging.ai", "c", ['com.whatsapp.vn'],function(obj, args) {
    //     send("on 111111()");
    //     var retval = this.apply(obj, args);
    //     return retval; 
    // });


    // $.hookMethod("com.whatsapp.uy", "a", ['int', 'java.lang.Object'],$.getHookImpl(true, true));

    // $.hookMethod("com.whatsapp.tl", "a", ['int', 'int'], function(obj, args) {
    //     send("on 33333()");
    //     var retval = this.apply(obj, args);
    //     return retval; 
    // });

    // $.hookMethod("com.whatsapp.tl", "a", ['java.lang.CharSequence', 'int'], $.getHookImpl(false, true)); 

    /////////////////////////// 定位相关 ////////////////////////////
    // $.hookMethods("dalvik.system.DexClassLoader", "$init", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeUpdates", $.getHookImpl(false, true)); 

    // $.hookMethods("android.location.LocationManager", "sendNiResponse", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "sendExtraCommand", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "getGpsStatus", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeGpsNavigationMessageListener", $.getHookImpl(false, true)); 

    // $.hookMethods("android.location.LocationManager", "addGpsNavigationMessageListener", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeGpsMeasurementListener", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "addGpsMeasurementListener", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeNmeaListener", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "addNmeaListener", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeGpsStatusListener", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "addGpsStatusListener", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "clearTestProviderStatus", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "setTestProviderStatus", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "addTestProvider", $.getHookImpl(false, true)); 

    // $.hookMethods("android.location.LocationManager", "setTestProviderEnabled", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "clearTestProviderLocation", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "setTestProviderLocation", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeTestProvider", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "getLastKnownLocation", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "getLastLocation", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "isProviderEnabled", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeAllGeofences", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "removeGeofence", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "addGeofence", $.getHookImpl(false, true)); 

    // $.hookMethods("android.location.LocationManager", "addProximityAlert", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "requestSingleUpdate", $.getHookImpl(false, true)); 
    // $.hookMethods("android.location.LocationManager", "requestLocationUpdates", $.getHookImpl(false, true)); 

    // $.hookMethods("android.location.LocationManager$ListenerTransport", "onLocationChanged", $.getHookImpl(false, true));   // 所有位置更新，都会从这里派发。
    

    /////////////////////////// 网络相关 4G ///////////////////////////
    // $.hookMethod("android.net.NetworkInfo", "getType", [], function(obj, args) {
    //     send("on getType()");
    //     // var retval = this.apply(obj, args);
    //     return 0; // TYPE_MOBILE: 0   TYPE_WIFI: 1

    // });
    // $.hookMethod("android.net.NetworkInfo", "getSubtype", [], function(obj, args) {
    //     send("on getSubtype()");
    //     // var retval = this.apply(obj, args);
    //     return 13;   // NETWORK_TYPE_LTE: 13    / WIFI: NETWORK_TYPE_UNKNOWN : 0
    // });

    // $.hookMethod("android.net.NetworkInfo", "getTypeName", [], function(obj, args) {
    //     send("on getTypeName()");
  
    //     return "MOBILE";  // WIFI: 'WIFI' 
    // });

    // $.hookMethod("android.net.NetworkInfo", "getSubtypeName", [], function(obj, args) {
    //     send("on getSubtypeName()");
  
    //     return "LTE";   // WIFI: ''
    // });

    // $.hookMethod("android.telephony.TelephonyManager", "getNetworkType", [], function(obj, args) {
    //     send("on getNetworkType()");
    //     // var retval = this.apply(obj, args);
    //     return 13;   // NETWORK_TYPE_LTE  / WIFI: NETWORK_TYPE_UNKNOWN : 0
    // });


    /////////////////////////// WIFI信息 ///////////////////////////
    // $.hookMethod("android.net.wifi.WifiManager", "isWifiEnabled", [], function(obj, args) {
    //     send("on isWifiEnabled()");
  
    //     return true; // true
    // });

    // $.hookMethod("android.net.wifi.WifiManager", "getWifiState", [], function(obj, args) {
    //     send("on isWifiEnabled()");
  
    //     return 3;   // WIFI_STATE_ENABLING
    // });

    // $.hookMethod("android.net.wifi.WifiInfo", "getNetworkId", [], function(obj, args) {
    //     send("on getNetworkId()");
  
    //     return 1; 
    // });

    // $.hookMethod("android.net.wifi.WifiInfo", "getSSID", [], function(obj, args) {
    //     send("on getSSID()");
  
    //     return "WeiQing2222"; 
    // });

    // $.hookMethod("android.net.wifi.WifiInfo", "getBSSID", [], function(obj, args) {
    //     send("on getBSSID()");
  
    //     return "04:18:d6:d3:c7:b5"; 
    // });

    // $.hookMethod("android.net.wifi.WifiInfo", "getMacAddress", [], function(obj, args) {
    //     send("on getMacAddress()");
  
    //     return "00:B2:00:00:00:A5"; 
    // });

    // $.hookMethod("android.net.wifi.WifiInfo", "getIpAddress", [], function(obj, args) {
    //     send("on getIpAddress()");
  
    //     return 1761716416;  // C0 A8 01 69 == 192.168.1.105
    // });  

    /////////////////////////// 屏蔽周边WIFI 扫描结果 //////////////////////////////
    // $.hookMethod("android.net.wifi.WifiManager", "getScanResults", [], function(obj, args) {
    //     send("on getScanResults()");
  
    //     return Java.use("java.util.ArrayList").$new();;  // 构造空结果，
    // });  

// $.hookClass("android.net.wifi.WifiInfo", $.getHookImpl(true, true));
// $.hookClass("android.net.wifi.WifiManager", $.getHookImpl(true, true));
    // $.hookMethod("com.baidu.location.Jni", "encodeTp4", ['java.lang.String'], function(obj, args) {
    //     send("on encodeTp4() " );
    //     send("before:");
    //     send(args);
    //     var data = "&nw=c&cl=460|13660|19|347&cl_s=-95&cdmall=114.0|30.0&cl_t=1603939635836&cs=5&sdk=7.72&addr=allj&sema=aptag|aptagd|&coor=gcj02&" + 
    //            "cu=406A34B18E7DB43BF63C673FF682478D|HQ24SLROV&Aim=86768602056128&snd=84B7N15A10011462&Aid=a3a1c2a7a746f9c4&fw=7.72&lt=1&mb=Nexus 6P&" + 
    //            "laip=0afb002b&resid=12&os=A23&sv=6.0.1&wf=0418d6d3c5b9;62;\"aaaa\"&wf_n=1&wf_gw=10.251.0.1&cn=32&prod=SDK6.0:com.baidu.baidulocationdemo|&lmd=2&bc=5&" + 
    //            "nc=&ki=WUj6BCSY9KM1hRznvVLFodrfFCQo7jlG&sn=F9:66:C2:53:E4:23:75:1C:3C:D2:4E:49:61:99:89:59:A4:2E:67:73;com.baidu.baidulocationdemo"; 
    //     args[0] = data;
    //     send("after:");
    //     send(args);
    //     var retval = this.apply(obj, args);
    //     send(retval);
    //     return retval;
    // });  

    // $.hookMethod("com.baidu.location.BDLocation", "getLatitude", [], function(obj, args) {
    //     send("on getLatitude()");
  
    //     return 39.820003;
    // }); 

    // $.hookMethod("com.baidu.location.BDLocation", "getLongitude", [], function(obj, args) {
    //     send("on getLongitude()");
  
    //     return 116.490000; 
    // });   

    // $.hookMethod("com.baidu.location.BDLocation", "getLocationDescribe", [], function(obj, args) {
    //     send("on getLocationDescribe()");
  
    //     return "";
    // });   

    // $.hookMethod("com.baidu.location.BDLocation", "getCountry", [], function(obj, args) {
    //     send("on getCountry()");
  
    //     return "中国";
    // }); 

    // $.hookMethod("com.baidu.location.BDLocation", "getCity", [], function(obj, args) {
    //     send("on getCity()");
  
    //     return "上海市";
    // }); 

    // $.hookMethod("com.baidu.location.BDLocation", "getDistrict", [], function(obj, args) {
    //     send("on getDistrict()");
  
    //     return "上海市";
    // }); 

    // $.hookMethod("com.baidu.location.BDLocation", "getStreet", [], function(obj, args) {
    //     send("on getStreet()");
  
    //     return "";
    // }); 

    // $.hookMethod("com.baidu.location.BDLocation", "getAddrStr", [], function(obj, args) {
    //     send("on getAddrStr()");
  
    //     return "中国上海市上海市";
    // }); 
    

    // $.hookClass("com.baidu.location.BDLocation", $.getHookImpl(true, true));
    var host = "10.251.0.65";
    var port = 8000;

    $.hookMethod("java.lang.System", "getProperty", ['java.lang.String'], function(obj, args) {
        
        if (args[0] == 'http.proxyHost' || args[0] == 'https.proxyHost' || args[0] == 'proxyHost') {
            send('on getProperty(' + args[0] + ')' );
            send('result: ' + host + '\n');
            return host;
        } else if (args[0] == 'http.proxyPort'|| args[0] == 'https.proxyPort' || args[0] == 'proxyPort') {
            send('on getProperty(' + args[0] + ')' );
            send('result: ' + port.toString() + '\n');
            return port.toString();
        } 

        send('on getProperty(' + args[0] + ')' );
        var retval = this.apply(obj, args);
        send('result: ' + retval + '\n');
        return retval;
    }); 

    $.hookMethod("android.net.Proxy", "getHost", ['android.content.Context'], function(obj, args) {
        send("on getHost()\n");
    
        return host;
    }); 

    $.hookMethod("android.net.Proxy", "getDefaultHost", [], function(obj, args) {
        send("on getDefaultHost()\n");
    
        return host;
    }); 


    $.hookMethod("android.net.Proxy", "getPort", ['android.content.Context'], function(obj, args) {
        send("on getPort()\n");
    
        return port;
    }); 

    $.hookMethod("android.net.Proxy", "getDefaultPort", [], function(obj, args) {
        send("on getDefaultPort()\n");
    
        return port;
    }); 

    $.hookMethod("java.net.Proxy", "type", [], function(obj, args) {
        send("on Proxy.type()\n");
    
        /*
         public enum Type {

            DIRECT,

            HTTP,
     
            SOCKS
        };
        */

        return Java.use("java.net.Proxy$Type").class.getDeclaredField("HTTP").get(null);;
    }); 
    // var a = Java.cast(, Java.use("java.net.Proxy$Type"));
    // var a = Java.use("java.net.Proxy$Type").class.getDeclaredField("HTTP").get(null);
    // send(a)
    // var member = Java.use("java.net.Proxy$Type").class.getDeclaredField("HTTP");
    // send(member);
    // members.forEach(function(member) {
    //     // 
    //     console.log("member: ", member);
    // });  

    // var ConstructorParam =Java.array('Ljava.lang.String;',[objectclass.class]);
    // var Constructor = hookClassCast.getDeclaredConstructor(ConstructorParam);

    $.hookMethod("java.net.Proxy", "address", [], function(obj, args) {
        send("on Proxy.address()");
        var inet_address = Java.use("java.net.InetSocketAddress").$new(host, port);
        send(inet_address.toString() + '\n');
        return inet_address;
    }); 
}); 
"""
dev_id = Adb.devices(True)[0]
frida_hooker = FridaHooker.instance(dev_id)
top_app = Adb.top_app(dev_id, Adb.get_sdk_level(dev_id))

id = frida_hooker.hook(top_app, js_code, True)
if id == -1:
    print('启动代理失败')
    exit(0)
print('正在代理, dev{} {}'.format(dev_id, top_app))

time.sleep(5)
frida_hooker.stop_hook_app(top_app)
print('代理已经停止')