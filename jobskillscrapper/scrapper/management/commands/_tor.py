'''
Python script to connect to Tor via Stem and Privoxy, requesting a new connection (hence a new IP as well) as desired.
'''
import urllib2

from stem import Signal
from stem.control import Controller


# request a URL
def request(url, headers):
    renew_connection()

    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({'http': '127.0.0.1:8118'})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    # request a URL
    # via the proxy
    _set_urlproxy()
    request = urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()


# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='alysfhknu')
        controller.signal(Signal.NEWNYM)
        controller.close()
