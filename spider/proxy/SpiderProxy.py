# -*- coding:utf-8 -*-

import lxml.html
from gevent import monkey
from gevent.pool import Pool
import urllib2
import requests

from mysql.MySQLHelper import MySQLHelper


class SpiderProxy(object):  # 爬取页面上的ip

    headers = {
        'Host': 'www.xicidaili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://www.xicidaili.com/wt/1"
    }

    def __init__(self, session_url):
        self.req = requests.session()
        self.req.get(session_url)

    def getHtml(self, url):
        html = self.req.get(url, headers=self.headers)
        return html.content

    def get_all_proxy(self, url, n):  # 取得所有1-n页上的代理IP
        data = []
        for i in range(1, n):
            html = self.getHtml(url + str(i))
            tree = lxml.html.fromstring(html)
            trs = tree.cssselect('tr.odd')
            for tds in trs:
                try:
                    data.append({tds[5].text : tds[1].text + ":" + tds[2].text})   # 协议 ip地址 端口
                except Exception as e:
                    pass
        return data

class IsActiveProxyIP(object):  # 用gevent 异步并发验证 代理IP是不是可以用

    def __init__(self, session_url):
        self.proxy = SpiderProxy(session_url)
        self.is_active_proxy_ip = []

    def probe_porxy_ip(self, proxy_ip):  # 代理检测
        proxy = urllib2.ProxyHandler(proxy_ip)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        try :
            html = urllib2.urlopen('http://1212.ip138.com/ic.asp')
            if html:
                self.is_active_proxy_ip.append(proxy_ip)
                return True
            else:
                return False
        except Exception as e:
            return False

class Proxies_to_db(object):

    def __init__(self):
        self.session_url = 'http://www.xicidaili.com/wt/1'
        self.url = 'http://www.xicidaili.com/wt/'

    def TO_DB(self, db):
        # 得到所有代理ip
        proxies = IsActiveProxyIP(self.session_url)
        ip_list = proxies.proxy.get_all_proxy(self.url, 2)

        # 异步并发
        pool = Pool(20)
        pool.map(proxies.probe_porxy_ip, ip_list)

        db.update('truncate table proxy')   # 清空表中数据 不可恢复
        for proxy_url in proxies.is_active_proxy_ip:
            sql = "insert into proxy(protocol,proxy_url) value('{}','{}')".format(proxy_url.keys()[0], proxy_url.values()[0])
            #print sql
            db.insert(sql)



















