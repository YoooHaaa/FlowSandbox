Java.perform(function () {

    var $ = new JavaHelper();
    var packageNameOfCurrentProcess = null;

    function showPropertyNames(obj) {
        Object.getOwnPropertyNames(obj).forEach(function(member) {
            console.log("member: ", member);
        });
    }

    function getProxyPackage(){
        var _packagename = Java.use("android.os.SystemProperties").get("sandbox.httpproxy.packagename");
        if (_packagename == null) {
            send("[ERR] didn't got the 'sandbox.httpproxy.packagename'")
        }
        return _packagename;
    }

    function getProxyHost(){
        var _host = Java.use("android.os.SystemProperties").get("sandbox.httpproxy.host");
        if (_host == null) {
            send("[ERR] didn't got the 'sandbox.httpproxy.host'")
        }
        return _host;
    }

    function getProxyPort(){
        var _port = Java.use("android.os.SystemProperties").get("sandbox.httpproxy.port");
        if (_port == null) {
            send("[ERR] didn't got the 'sandbox.httpproxy.port'")
        }
        return Number(_port);
    }

    function isCurrentPackageTurnOn() {
        return getProxyPackage() == packageNameOfCurrentProcess;
    }

    // var port  = 8000;
    $.hookMethod("java.lang.System", "getProperty", ['java.lang.String'], function(obj, args) {
        if (!isCurrentPackageTurnOn()) {
            send('current package is turned off');
            return this.apply(obj, args);
        }

        var host = getProxyHost();
        var port = getProxyPort();

        //send('on getProperty(' + args[0] + ')' );

        if (args[0] == 'http.proxyHost' || args[0] == 'https.proxyHost' || args[0] == 'proxyHost' || args[0] == 'bifrost.proxyHost') {
            send('result: ' + host + '\n');
            return host;
        } else if (args[0] == 'http.proxyPort'|| args[0] == 'https.proxyPort' || args[0] == 'proxyPort' || args[0] == 'bifrost.proxyPort') {
            send('result: ' + port.toString() + '\n');
            return port.toString();
        }

        var retval = this.apply(obj, args);
        //send('result: ' + retval + '\n');
        return retval;
    });

    $.hookMethod("android.net.Proxy", "getHost", ['android.content.Context'], function(obj, args) {
        // send("on getHost()\n");
        if (!isCurrentPackageTurnOn()) {
            send('current package is turned off');
            return this.apply(obj, args);
        }

        var host = getProxyHost();
        return host;
    });

    $.hookMethod("android.net.Proxy", "getDefaultHost", [], function(obj, args) {
        // send("on getDefaultHost()\n");
        if (!isCurrentPackageTurnOn()) {
            send('current package is turned off');
            return this.apply(obj, args);
        }

        var host = getProxyHost();
        return host;
    });


    $.hookMethod("android.net.Proxy", "getPort", ['android.content.Context'], function(obj, args) {
        // send("on getPort()\n");
        if (!isCurrentPackageTurnOn()) {
            send('current package is turned off');
            return this.apply(obj, args);
        }

        var port = getProxyPort();
        return port;
    });

    $.hookMethod("android.net.Proxy", "getDefaultPort", [], function(obj, args) {
        // send("on getDefaultPort()\n");
        if (!isCurrentPackageTurnOn()) {
            send('current package is turned off');
            return this.apply(obj, args);
        }

        var port = getProxyPort();
        return port;
    });

    $.hookMethod("java.net.Proxy", "type", [], function(obj, args) {
        // send("on Proxy.type()\n");
        if (!isCurrentPackageTurnOn()) {
            send('current package is turned off');
            return Java.use("java.net.Proxy$Type").class.getDeclaredField("DIRECT").get(null);
        }

        /*
        public enum Type {

         DIRECT,

         HTTP,

         SOCKS
        };
        */

        return Java.use("java.net.Proxy$Type").class.getDeclaredField("HTTP").get(null);
    });

    $.hookMethod("java.net.Proxy", "address", [], function(obj, args) {
        // send("on Proxy.address()");
        if (!isCurrentPackageTurnOn()) {
            send('current package is turned off');
            return this.apply(obj, args);
        }

        var host = getProxyHost();
        var port = getProxyPort();
        return Java.use("java.net.InetSocketAddress").$new(host, port);
    });


    /////////////////////////////////////// entry ///////////////////////////////////////
    function OnApplicationCreate(context) {
        var _context = Java.retain(context);
        packageNameOfCurrentProcess = _context.getPackageName();
    }

    ////////////////////////////////////// resolve context /////////////////////////////////
    var tmp_context = null;
    $.hookMethod("android.content.ContextWrapper", "$init", ['android.content.Context'], function (obj, args) {
        send("on ContextWrapper()");
        var retval = this.apply(obj, args);
        if (tmp_context == null) {
            tmp_context = obj;
            OnApplicationCreate(obj);
        }
        return retval;

    });

    $.hookMethod("android.content.ContextWrapper", "attachBaseContext", ['android.content.Context'], function (obj, args) {
        send("on attachBaseContext()");
        var retval = this.apply(obj, args);
        if (tmp_context == null) {
            tmp_context = obj;
            OnApplicationCreate(obj);
        }
        return retval;
    });

});