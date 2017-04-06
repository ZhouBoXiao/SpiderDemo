# -*- coding:utf-8 -*-


import urlparse
import urllib2
import random
import time
from datetime import datetime, timedelta
import socket

DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
DEFAULT_DELAY = 1
DEFAULT_RETRIES = 5
DEFAULT_TIMEOUT = 60


class Downloader(object):
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(5)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # 错误
                    result = None
        if result is None:
            # result 为空则要下载
            #self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None  # 随机选择一个代理ip

            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                # 把结果存储在cache里
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        print '下载:', url
        request = urllib2.Request(url, data, headers or {})
        opener = self.opener or urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}  # 设置代理  proxy_params是个字典
            print proxy_params
            opener.add_handler(urllib2.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            print 'Download error:', str(e)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # 等待5s 然后重试一遍
                    self.throttle.wait(5)
                    return self.download(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {'html': html, 'code': code}


class Throttle(object):


    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, sleep_secs):
        time.sleep(sleep_secs)
        '''
        domain = urlparse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()
        '''