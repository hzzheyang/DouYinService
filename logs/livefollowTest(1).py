import json

import requests

params = {
    "webcast_sdk_version":"1150",
    "manifest_version_code":"750",
    "app_type":"normal",
    "iid":"2840785756890477", #改成自己的 找到
    "channel":"wandoujia_aweme2",
    "device_type":"HWI-AL00",
    "language":"zh",
    "uuid":"869294590508213", #改成自己的 找到 x
    "resolution":"1080*2160",
    "openudid":"23fb4303cca10428", #改成自己的 找到
    "update_version_code":"7502",
    "os_api":"28",
    "dpi":"480",
    "ac":"wifi",
    "device_id":"69631755224", #改成自己的 找到
    "mcc_mnc":"46001",
    "os_version":"9",
    "version_code":"750",
    "app_name":"aweme",
    "version_name":"7.5.0",
    "js_sdk_version":"1.19.4.16",
    "device_brand":"HUAWEI",
    "ssmix":"a",
    "device_platform":"android",
    "aid":"1128"
}

sec_uid = 'MS4wLjABAAAAOdlL1e_rshAFPkMXy1SaBEJSoEeFCgtida6ZX-yljQ0' # 被关注人sec_uid 找到
sid_guard = '430a5af080cac9ce120177b9c83fd6c7%7C1591865992%7C5184000%7CMon%2C+10-Aug-2020+08%3A59%3A52+GMT'#自己的sec_uid 找到
proxy = '58.218.200.248:8236'# 代理IP

url = "http://47.108.87.251:5500/liveFollow/user/follow?sec_uid="+sec_uid+"&sid_guard="+sid_guard+"&proxyip="+proxy

resp = requests.post(url=url, data=params)
print(resp.status_code)
print(resp.text)

