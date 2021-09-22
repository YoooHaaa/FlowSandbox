Java.perform(function () {
    var $ = new JavaHelper();
    var g_packageName = null;

    $.hookMethods("java.io.File", "$init", function(obj, args) {
        // send("on File()\n");
        var instance = this.apply(obj, args);
        var path = obj.getPath();  // 构造完成后，再直接获取路径.兼容4个重载构造函数:(String) (String,String) (File, String) (URI)
        if (path == "/system/etc/security/cacerts/${mitm_cert_hash_name}") {
            var mitm_cert_path = "${mitm_cert_path}"
            obj.path.value = mitm_cert_path
            // send("use cert of mitmproxy: " + obj.path.value );
        }
        return instance;
    });

    /////////////////////////////////////// entry ///////////////////////////////////////
    function OnApplicationCreate(context) {
        if (g_packageName != null) {
            return;
        }
        g_packageName = context.getPackageName();
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
