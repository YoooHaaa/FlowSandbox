import base64
from urllib.parse import urlparse

import mitmproxy.http

proxy_data = urlparse('http://sandbox:7481590263@39.104.55.246:8888')
auth = proxy_data.username + ':' + proxy_data.password
authLine = "Basic" + " " + base64.b64encode(auth.encode()).decode()


def request(flow: mitmproxy.http.HTTPFlow) -> None:
    # print('Request: ' + flow.request.url)
    pass


def response(flow: mitmproxy.http.HTTPFlow) -> None:
    # print('Response: ' + flow.request.url)
    if 'toutiao' in flow.request.url:
        flow.response.content = b''
        # print("block toutiao url: " + c_flow.request.url)
    elif 'kuaishou' in flow.request.url:
        flow.response.content = b''
    elif 'gdt.qq.com' in flow.request.url:
        flow.response.content = b''
    # elif 'mob.com' in c_flow.request.url:
    #     flow.response.content = b''
    pass
