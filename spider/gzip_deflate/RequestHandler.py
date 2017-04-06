# -*- coding:utf-8 -*-
# E:/PycharmProjects/
# create by boxiao on 2016/12/29

from gzip import GzipFile
import urllib2
from StringIO import StringIO
import zlib

class ContentEncodingProcessor(urllib2.BaseHandler):
    def http_request(self, req):
        req.addheader('Accept-Encoding', 'gzip, deflate')
        return req

    def http_response(self, req, resp):
        old_resp = resp
        # gzip
        if resp.headers.get('content-encoding') == 'gzip':
            gz = GzipFile(
                fileobj=StringIO(resp.read()),
                mode='r'
            )
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
        # deflate
        if resp.headers.get('content-encoding') == 'deflate':
            gz = StringIO(deflate(resp.read()))
            resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
            resp.msg = old_resp.msg
        return resp

    # deflate support


    def deflate(self, data):
        try:
            return zlib.decompress(data, -zlib.MAX_WBITS)
        except zlib.error:
            return zlib.decompress(data)

if __name__ == '__main__':
    url = 'https://github.com/xxg1413/python/blob/master/%E5%8D%9A%E5%AE%A2/python%E7%88%AC%E8%99%AB%E6%8A%93%E7%AB%99%E7%9A%84%E6%80%BB%E7%BB%93.pdf'
    encoding_support = ContentEncodingProcessor()
    opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
    content = opener.open(url).read()
    print content