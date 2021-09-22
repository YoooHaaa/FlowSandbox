<!--
 * @Author: Rodney Cheung
 * @Date: 2020-08-28 10:07:54
 * @LastEditors: Rodney Cheung
 * @LastEditTime: 2020-08-28 14:11:46
 * @FilePath: /Wesker/Users/jsrdzhk/workspace/Tweezer/tweezer/README.md
-->
# README

## 一、项目简介

tweezer通过mitmproxy将proxydroid劫持的流量转发到pc，并利用pc对流量包进行解析，它还支持自定义插件扩展功能。

## 二、先决条件

1. PC安装Python 3.5及以上
2. 手机使用USB连接PC，并允许debug调试
3. 手机需要root，且是应用可获取的root，aosp编译的手机不行（应用无法获取root权限）
4. 如果是windows环境：

a). 安装python时需要勾选`Add Python to environment variables`，来保证命令能够加入环境变量。

![pic](./readme_pic/1.jpg)

   b). 需要安装`Microsoft Visual C++`运行库，保证加解密库能够正常运行。
       下载地址： https://visualstudio.microsoft.com/zh-hans/downloads, 一路默认下一步安装。

![pic](./readme_pic/2.jpg)


![pic](./readme_pic/3.jpg)


## 三、如何root手机

### 3.1 TWRP+Magisk方式

确保手机bootloader锁已经解开，下载手机对应型号的TWRP，并去`Magisk`网站下载`Magisk-xx.zip`。将`Magisk`安装包push到手机的`/sdcard/Download`目录下，然后执行以下步骤:
```shell script
adb reboot bootloader
fastboot flash twrp-xxx.img
fastboot boot twrp-xxx.img
```
之后手机会进入twrp页面，点击`Install`，并选择`Magisk`的安装包，等待安装完成，重启手机即可。

### 3.2 auto cf root方式

`Google`搜索`auto cf root`，进网站自己搜索设备型号，注意看准设备的build numbers和Android version，如果点进去没有自动root的脚本，那就是没办法用auto cf root，如果有，直接下载解压，执行目录下的脚本即可。

## 四、如何使用

1. 使用`pip install tweezer-xxx.whl`安装`tweezer`，之后直接在命令行使用`tweezer`运行即可，`unix`平台需要`sudo`权限。
2. 根据提示选择中间人代理使用的网卡（一般不需要选）
3. 等待插件加载完成并提示开始监控app时就可以打开app开始使用了

## 五、输出产物

沙箱启动后会在当前工作目录生成一个tweezer文件夹，其结构如下:

```
.
├── config //配置文件
│   ├── known_ad_platforms.json //已知广告配置文件，不需要使用
│   └── tweezer_conf.json //主要配置文件
├── log //日志
│   ├── debug.log
│   ├── error.log
│   ├── info.log
│   └── warning.log
├── output //广告信息抓取存储目录
│   └── 2020-11-05_13-46-22
├── plugin //插件（开发人员调试使用）
│   ├── __init__.py
│   ├── __pycache__
│   ├── ad
│   ├── base
│   ├── general
│   └── hotkey
└── rules //插件规则（开发人员调试使用）
    ├── ad_filter_rules.json
    ├── gdt_ad_cap_rules.json
    ├── packet_filter_rules.json
    ├── tuia_ad_cap_rules.json
    ├── url_filter_rules.json
    └── weli_ad_cap_rules.json
```


目前所有广告件取证信息都在当前工作目录下的`tweezer/output`目录,对于每一个应用，如果抓取到了广告，就会生成结构如下的目录:
```
.
└── 2020-11-05_13-46-22
    └── 诸葛万年历 //app名称
        ├── 快手 //广告件名称
        │   └── output.json  //广告件输出
        ├── 广点通
        │   ├── gdt_err_response.txt
        │   └── output.json
        └── 百青藤
            └── output.json
```
`output.json`以json的格式存储了抓取到的相关信息

以快手为例：
```json
{
    "执行环境信息": {
        "设备型号": "Pixel 2",
        "SDK号": 27,
        "流量类型": "WIFI",
        "IP": "上海",
        "GPS": "上海浦东新区"
    },
    "SDK信息": {
        "广告SDK名称": "快手",
        "广告SDK版本": "0.6"
    },
    "APK信息": {
        "包名": "com.geek.luck.calendar.app",
        "应用名": "诸葛万年历",
        "版本号": "4.3.1"
    },
    "广告信息": [
        {
            "抓取时间": "2020-11-05_13-46-41",
            "uuid": "47c84be6-1f2a-11eb-9c85-acde48001122",
            "广告取证": {
                "标题": "寻位",
                "描述": "学会这一招,3s定位他的实时位位置!",
                "广告URL": "https://js.a.kspkg.com/ks/ad/third/7bc54c57-000a-471d-b060-d5619555d377.apk",
                "广告截图URL": "",
                "广告图片URL列表": [
                    "http://static.yximgs.com/udata/pkg/486ad703f54e4a398030f65fe1cd061c.png",
                    "https://txmov2.a.yximgs.com/upic/2020/09/10/16/BMjAyMDA5MTAxNjQwMDRfMTU3NzAwMTU3NV8zNTc5ODkwNTY3OF8wXzM=_b_B1453318c6b007691c9ea00a83234b450.mp4?tag=1-1604553730-unknown-0-ob2vxmkgcv-c859b554a8aa27dc&clientCacheKey=3xdtuu5t76issnw_b.mp4&tt=b&di=27609f9e&bp=13290",
                    "https://ali2.a.yximgs.com/bs2/multicover/735874320249108.jpg",
                    "https://tx2.a.yximgs.com/upic/2020/09/10/16/BMjAyMDA5MTAxNjQwMDRfMTU3NzAwMTU3NV8zNTc5ODkwNTY3OF8wXzM=_ff_Bee576fe6b6c5356969bf7ef896daee5e.webp?tag=1-1604553730-unknown-0-egajb2eram-2d6bde45fcf8f39f&clientCacheKey=3xdtuu5t76issnw_ff.webp&di=27609f9e&bp=13290"
                ],
                "广告图片存放路径": {},
                "广告网络包": ""
            },
            "可选广告信息": {
                "长度": 1280,
                "宽度": 720,
                "公司名": "济南泰如网络科技有限公司",
                "广告位ID": "",
                "广告类型": "NONE",
                "广告场景": ""
            }
        }
    ]
}
```

## 六、配置文件使用

在沙箱运行的工作目录会有一个`tweezer/config/tweezer_conf.json`文件，里面存储了沙箱的配置，简单对配置项进行介绍。

```json
{
  "script": { //启动脚本配置
    "emulator": { //模拟器脚本配置，配置模拟器的地址（模拟器还存在问题）
      "host": "127.0.0.1",
      "port": 7555
    }
  },
  "plugins": { //插件配置，主要用于控制插件是否加载以及插件使用的一些变量
    "general": { //通用插件配置
      "enabled": false, //开关
      "ad_filter": { // 模糊广告匹配插件（通过正则匹配URL，完成广告广告平台的发现）
        "enabled": true,
        "name": "AdFilter",
        "config": {
        }
      }
    },
    "ad": { //广告插件
      "enabled": true,
      "gdt_ad_cap": { //广点通插件
        "enabled": true,
        "name": "GdtAdCap",
        "config": {
        }
      },
      "tuia_ad_cap": { //推啊插件
        "enabled": true,
        "name": "TuiaAdCap",
        "config": {
          "capture_delay_time": 1 //自动截图的延时（防止网络环境不佳造成落地页没有加载出来就截图了）
        }
      },
      "qutoutiao_ad_cap": { //趣头条插件
        "enabled": true,
        "name": "QutoutiaoAdCap",
        "config": {
          "capture_delay_time": 2 //同上
        }
      },
      "toutiao_ad_cap": { //头条插件
        "enabled": true,
        "name": "ToutiaoAdCap",
        "config": {
          "capture_delay_time": 2 //同上
        }
      },
      "weli_ad_cap": { //微鲤广告插件
        "enabled": true,
        "name": "WeliAdCap",
        "config": {
        }
      },
      "kuaishou_ad_cap": { //快手广告插件
        "enabled": true,
        "name": "KuaishouAdCap",
        "config": {
          "capture_delay_time": 2 //同上
        }
      },
      "baidu_ad_cap": { //百度广告插件
        "enabled": true,
        "name": "BaiduAdCap",
        "config": {
          "capture_delay_time": 3 //同上
        }
      }
    },
    "hotkey": { //热键广告插件
      "enabled": true,
      "hotkey_screen_cap": {
        "enabled": true,
        "name": "HotkeyScreenCap",//截图广告插件，按下后会截取当前屏幕
        "config": {
          "shortcut": "default" //快捷键设置，以ctrl+j的格式可以自行定义快捷键
        }
      },
      "hotkey_packet_cap": {//保存广告包
        "enabled": true,
        "name": "HotkeyPacketCap",
        "config": {
          "shortcut": "default",
          "packet_cache_size": 10000
        }
      },
      "hotkey_switch_net_traffic": {//伪装网络环境，里面配置不需要改动
        "enabled": false,
        "name": "HotkeySwitchNetTraffic",
        "config": {
          "shortcut": "default",
          "wifi": {
            "ssid": "weiqing",
            "bssid": "04:18:d6:d3:c7:b5",
            "mac": "00:B2:00:00:00:A5",
            "ip": "192.168.1.1"
          }
        }
      },
      "hotkey_switch_location": {//代理插件
        "enabled": false,
        "name": "HotkeySwitchLocation",
        "config": {
          "shortcut": "default",
          "proxy_servers": [//可选的代理信息
            {
              "server": {
                "host": "39.104.55.246",
                "port": 8888,
                "user": "sandbox",
                "pwd": "7481590263"
              },
              "area": {
                "province": "内蒙古自治区",
                "city": "呼和浩特市"
              }
            }
          ]
        }
      }
    }
  },
  "no_proxy_apps": [//不会被沙箱监控的app，一般为系统app
    "com.android.providers.telephony",
    "com.android.providers.calendar",
    "com.android.providers.media",
    "org.proxydroid",
    "com.android.wallpapercropper",
    "com.android.voicedialer",
    "com.android.documentsui",
    "com.android.galaxy4",
    "com.android.externalstorage",
    "com.android.htmlviewer",
    "com.android.quicksearchbox",
    "com.android.mms.service",
    "com.android.providers.downloads",
    "com.android.browser",
    "com.android.soundrecorder",
    "com.android.defcontainer",
    "com.android.providers.downloads.ui",
    "com.android.pacprocessor",
    "com.android.certinstaller",
    "android",
    "com.android.contacts",
    "com.android.camera2",
    "com.android.mms",
    "com.android.nfc",
    "com.android.launcher3",
    "com.android.backupconfirm",
    "com.android.provision",
    "com.android.wallpaper.holospiral",
    "com.android.calendar",
    "com.android.phasebeam",
    "com.koushikdutta.vysor",
    "com.android.providers.settings",
    "com.android.sharedstoragebackup",
    "com.android.printspooler",
    "com.android.dreams.basic",
    "com.android.webview",
    "com.android.inputdevices",
    "com.estrongs.android.pop",
    "com.android.musicfx",
    "com.android.onetimeinitializer",
    "com.android.server.telecom",
    "com.android.keychain",
    "com.android.dialer",
    "com.android.gallery3d",
    "com.android.packageinstaller",
    "com.svox.pico",
    "com.android.proxyhandler",
    "com.android.inputmethod.latin",
    "com.android.musicvis",
    "com.android.managedprovisioning",
    "com.android.dreams.phototable",
    "com.android.noisefield",
    "com.android.smspush",
    "com.android.wallpaper.livepicker",
    "com.android.apps.tag",
    "jp.co.omronsoft.openwnn",
    "com.android.settings",
    "com.example.vivobackupservice_poc",
    "com.android.calculator2",
    "com.android.wallpaper",
    "com.android.vpndialogs",
    "com.android.email",
    "eu.chainfire.supersu",
    "com.android.music",
    "com.android.phone",
    "com.android.shell",
    "com.android.providers.userdictionary",
    "com.android.location.fused",
    "com.android.deskclock",
    "com.android.systemui",
    "com.android.exchange",
    "com.android.bluetooth",
    "com.android.providers.contacts",
    "com.android.captiveportallogin",
    "android.task.browser",
    "com.google.android.googlequicksearchbox",
    "com.google.android.packageinstaller",
    "com.miui.packageinstaller",
    "com.miui.home",
    "com.lbe.security.miui",
    "com.pkiller.mocklocation"
  ],
  "is_drop_known_ad_platform_flow": false
}
```

## 七、插件简介

### 7.1 广告模糊匹配插件

该插件使用自定义的规则匹配URL，并将匹配的结果存储在`sqlite3`数据库中。目前规则存放在`tweezer/resource/rules/ad_filter_rules/`中，如需添加自定义规则，可以新建一个文件，并将规则按行书写（匹配规则使用标准正则表达式）。该插件的输出在`result.db`中的`ad_url`表中。

### 7.2 手动截图

该插件添加了键盘快捷键截图功能，在Mac OS下快捷键为`Command + S`，其他平台则是`Alt + S`。

### 7.3 手动封包

该插件添加了键盘快捷键封包功能，在Mac OS下快捷键为`Command + C`，其他平台则是`Alt + C`。

### 7.4 网络环境伪装插件

该插件用于伪装手机的网络环境，如果加载了该插件，会在第一次启动时让用户选择网络环境。启动之后可以使用快捷键（在Mac OS下快捷键为`Command + L`，其他平台则是`Alt + L`）在Wi-Fi和蜂窝数据之间切换。

### 7.5 位置伪装插件

该插件用于切换设备的位置（IP和GPS），如果加载了该插件，会在第一次启动时让用户选择位置。启动之后可以使用快捷键（在Mac OS下快捷键为`Command + J`，其他平台则是`Alt + J`）在配置文件中配置的位置中随机切换（目前仅有一个代理服务器）。
