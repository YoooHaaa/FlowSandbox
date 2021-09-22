import mitmproxy.http
from mitmproxy.utils import strutils
from urllib.parse import urlparse
import base64

proxy_data = urlparse('http://sandbox:7481590263@39.104.55.246:8888')
auth = proxy_data.username + ':' + proxy_data.password
authLine = "Basic" + " " + base64.b64encode(auth.encode()).decode()


def request(flow: mitmproxy.http.HTTPFlow) -> None:
    print('Request: ' + flow.request.method)
    if flow.request.method == "CONNECT":
        # If the decision is done by domain, one could also modify the server address here.
        # We do it after CONNECT here to have the request data available as well.
        print('CONTENT..')
        print(flow.live)
        return

    if flow.live:
        print('Setting upstream proxy to ' + proxy_data.hostname + ' and port ' + str(proxy_data.port))
        flow.live.change_upstream_proxy_server((proxy_data.hostname, proxy_data.port))
        flow.request.headers["Proxy-Authorization"] = authLine

    pass

def response(flow: mitmproxy.http.HTTPFlow) -> None:

    pass
