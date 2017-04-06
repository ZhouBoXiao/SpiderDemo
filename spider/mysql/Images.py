# -*- coding:utf-8 -*-

import random
import uuid

import MySQLdb
import PyV8
import time
import logging.config

from downloader import Downloader
from mysql.MySQLHelper import MySQLHelper

class Images:

    def __init__(self):
        self.D = Downloader(delay=0, user_agent='', proxies='', num_retries=3, timeout=60)
        self.db = MySQLHelper()
        self.ctxt = PyV8.JSContext()
        self.ctxt.enter()

    def common(self, pic_url, tablename): #　得到完整的url存入数据库
        pic_ = self.D(pic_url)
        string = MySQLdb.escape_string(pic_)
        sql = "insert into "+tablename+"(image_url,image_data) value('%s', '%s')" % (pic_url, string)
        self.db.insert(sql)  # 存入数据库

    def xinjiang_images(self, pic_nums=20):   # 新疆
        url = 'http://gsxt.xjaic.gov.cn:7001/ztxy.do?method=createYzm'  # http://gsxt.xjaic.gov.cn:7001/ztxy.do?method=createYzm&dt=1481621583421&random=1481621583421
        #for _ in xrange(pic_nums):
        urlpattern = str(time.time()).replace('.', '')
        pic_url = url + '&dt=' + urlpattern + '&random=' + urlpattern
         #   self.common(pic_url, 'xinjiang_images')
        return pic_url

    def ningxia_images(self, pic_nums=20):   # 宁夏
        url = 'http://gsxt.ngsh.gov.cn/ECPS/verificationCode.jsp'  # http://gsxt.ngsh.gov.cn/ECPS/verificationCode.jsp?_=1481621422850
        #for _ in xrange(pic_nums):
        pic_url = url + '?_=' + str(time.time()).replace('.', '')
           # self.common(pic_url, 'ningxia_images')
        return pic_url

    def sichuan_images(self, pic_nums=20):   # 四川
        url = 'http://gsxt.scaic.gov.cn/ztxy.do?method=createYzm3'  # http://gsxt.scaic.gov.cn/ztxy.do?method=createYzm3&dt=1481621168364&random=1481621168364
        #for _ in xrange(pic_nums):
        urlpattern = str(time.time()).replace('.', '')
        pic_url = url + '&dt=' + urlpattern + '&random=' + urlpattern
           # self.common(pic_url, 'sichuan_images')
        return pic_url

    def chongqing_images(self, pic_nums=20):   # 重庆
        url = 'http://gsxt.cqgs.gov.cn/sc.action?width=130&height=40&fs=23'   # http://gsxt.cqgs.gov.cn/sc.action?width=130&height=40&fs=23&t=1481621014973
        #for _ in xrange(pic_nums):
        pic_url = url + '&t=' + str(time.time()).replace('.', '')
        #    self.common(pic_url, 'chongqing_images')
        return pic_url

    def hunan_images(self, pic_nums=20):   # 湖南
        url = 'http://gsxt.hnaic.gov.cn/notice/captcha'  # http://gsxt.hnaic.gov.cn/notice/captcha?preset=&ra=0.5890322648352662
        #for _ in xrange(pic_nums):
        pic_url = url + '?preset=&ra=' + random.random()
           # self.common(pic_url, 'hunan_images')
        return pic_url

    def hainan_images(self, pic_nums=20):   # 广东
        url = 'http://aic.hainan.gov.cn:1888/validateCode.jspx?type=0'  #http://aic.hainan.gov.cn:1888/validateCode.jspx?type=0&id=0.48870362925152677
        #for _ in xrange(pic_nums):
        pic_url = url + '?id=' + random.random()
           # self.common(pic_url, 'hainan_images')
        return pic_url

    def guangdong_images(self, pic_nums=20):   # 广东
        url = 'http://gsxt.gdgs.gov.cn/aiccips/verify.html'
        #for _ in xrange(pic_nums):
        pic_url = url + '?random=' + random.random()   #http://gsxt.gdgs.gov.cn/aiccips/verify.html?random=0.752980708349893
            #self.common(pic_url, 'guangdong_images')
        return pic_url

    def shandong_images(self, pic_nums=20):   # 山东
        url = 'http://218.57.139.24/securitycode'  #http://218.57.139.24/securitycode?0.05817280571462424
        #for _ in xrange(pic_nums):
        pic_url = url + '?' + random.random()
        #self.common(pic_url, 'shandong_images')
        return pic_url

    def jiangxi_images(self, pic_nums=20):   # 江西
        url = 'http://gsxt.jxaic.gov.cn/warningetp/reqyzm.do' # http://gsxt.jxaic.gov.cn/warningetp/reqyzm.do?r=1481619111453
        #for _ in xrange(pic_nums):
        pic_url = url + '?r=' + str(time.time()).replace('.', '')
        #self.common(pic_url, 'jiangxi_images')
        return pic_url

    def fujian_images(self, pic_nums=20):   # 福建
        url = 'http://wsgs.fjaic.gov.cn/creditpub/captcha?preset=str-01,math-01' #http://wsgs.fjaic.gov.cn/creditpub/captcha?preset=str-01,math-01&ra=0.8477420096943082
        #for _ in xrange(pic_nums):
        pic_url = url + '&ra=' + random.random()
            #self.common(pic_url, 'fujian_images')
        return pic_url

    def jiangsu_pattern(self):
        func = self.ctxt.eval('''(function(){return new Date()})''')
        return str(func())

    def jiangsu_images(self, pic_nums=20):   # 江苏
        url = 'http://www.jsgsj.gov.cn:58888/province/rand_img.jsp?type=7' # <img border=\"0\" src=\"" + basePath+ "/rand_img.jsp?type=" + param + "&temp=" + new Date()
        #for _ in xrange(pic_nums):
        pic_url = url + '&temp=' + self.jiangsu_pattern()
         #   self.common(pic_url, 'jiangsu_images')
        return pic_url

    def shanghai_images(self, pic_nums=20):   # 上海
        url = 'https://www.sgs.gov.cn/notice/captcha?preset='
        #for _ in xrange(pic_nums):
        pic_url = url + '&ra=' + random.random()
         #   self.common(pic_url, 'shanghai_images')
        return pic_url

    def liaoning_pattern(self):
        func = self.ctxt.eval('''(function(){return Math.round(Math.random(100)*100000)})''')
        return str(func())

    def liaoning_images(self, pic_nums=20):   # 辽宁
        url = 'http://gsxt.lngs.gov.cn/saicpub/commonsSC/loginDC/securityCode.action'
        #for _ in xrange(pic_nums):
        pic_url = url + '?tdate=' + self.liaoning_pattern()
            #self.common(pic_url, 'liaoning_images')
        return pic_url

    def neimenggu_images(self, pic_nums=20):   # 内蒙古
        url = 'http://www.nmgs.gov.cn:7001/aiccips/verify.html'
        #for _ in xrange(pic_nums):
        pic_url = url + '?random=' + random.random()
        #self.common(pic_url, 'neimenggu_images')
        return pic_url

    def shanxi_images(self, pic_nums=20):  # 山西
        url = 'http://gsxt.sxaic.gov.cn/validateCode.jspx?type=0'   # /validateCode.jspx?type=0&id=0.29058256972867147
        #for _ in xrange(pic_nums):
        pic_url = url + '&id=' + random.random()
            #self.common(pic_url, 'shanxi_images')
        return pic_url

    def beijing_pattern(self):
        func = self.ctxt.eval('''(function(){return Math.ceil(Math.random()*100000)})''')
        return str(func())

    def beijing_images(self, pic_nums=20):   # 北京
        url = 'http://qyxy.baic.gov.cn/CheckCodeYunSuan?currentTimeMillis=1481555147807' # /CheckCodeCaptcha?currentTimeMillis=1481613218532&num=29526
        #for _ in xrange(pic_nums):   # 将北京的验证码存入beijing_images表中
        pic_url = url+'&num=' + self.beijing_pattern()
            #self.common(pic_url, 'beijing_images')
        return pic_url

    def tianjing_images(self, pic_nums=20):   # 天津
        url = 'http://tjcredit.gov.cn/verifycode'  # /verifycode?date=1481613853269
        #for _ in xrange(pic_nums):
        pic_url = url + '?date=' + str(time.time()).replace('.', '')
        #self.common(pic_url, 'tianjing_images')
        return pic_url



#　从数据库中读出图片
'''
sql = 'select image_data from images'
images = db.query(sql)
for image in images:
    pic_name = str(uuid.uuid1()) + '.jpg'
    #print image.image_data
    with open('../pic1/' +pic_name, 'wb') as f:
        f.write(image[0])
'''
# setHash("pt="+dcp.core.friend.friend.friend.pt+"&type=query&name="+name+"&sex="+sex+"&unitId="+unitId);
#setHash("pt=myfriend&type=query&name=周博孝&sex=0&unitId=")

#/portal/portal&p=friend&ac=4#pt=query&type=query&name=周博&sex=0&unitId=