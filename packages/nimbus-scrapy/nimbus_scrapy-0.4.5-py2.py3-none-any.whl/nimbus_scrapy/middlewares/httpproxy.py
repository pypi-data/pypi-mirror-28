# -*- coding: utf-8 -*-
from __future__ import absolute_import

from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed

try:
    from urllib2 import _parse_proxy
except ImportError:
    from urllib.request import _parse_proxy
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware as SHttpProxyMiddleware


class HttpProxyMiddleware(SHttpProxyMiddleware):
    EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                  ConnectionRefusedError, ConnectionDone, ConnectError,
                  ConnectionLost, TCPTimedOutError, ResponseFailed,
                  IOError, TunnelError)
    custorm_proxys = {}
    retry_http_codes = set()

    def __init__(self, settings=None, auth_encoding='latin-1'):
        super(HttpProxyMiddleware, self).__init__(auth_encoding)
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING')
        return cls(crawler.settings, auth_encoding=auth_encoding)

    def process_request(self, request, spider):
        if 'proxy' in request.meta:
            if request.meta['proxy'] is None:
                return
            # extract credentials if present
            creds, proxy_url = self._get_proxy(request.meta['proxy'], '')
            request.meta['proxy'] = proxy_url
            if creds and not request.headers.get('Proxy-Authorization'):
                request.headers['Proxy-Authorization'] = b'Basic ' + creds
            return
        return super(HttpProxyMiddleware, self).process_request(request, spider)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry_change_proxy(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS) and not request.meta.get('dont_retry', False):
            return self._retry_change_proxy(request, exception, spider)

    def _retry_change_proxy(self, request, reason, spider):
        pop_proxy = getattr(spider, "pop_proxy", None)
        proxy = None
        if property and callable(pop_proxy):
            proxy = pop_proxy()
            if proxy and isinstance(proxy, (list, tuple)) and len(proxy) >= 1:
                proxy = proxy[1]
        if proxy:
            creds, proxy_url = self._get_proxy(proxy, '')
            request.meta['proxy'] = proxy_url