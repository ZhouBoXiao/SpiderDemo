# -*- coding:utf-8 -*-


import multiprocessing
import threading
import time
import uuid

from mysql.Images import Images
from proxy.SpiderProxy import Proxies_to_db
from mysql.MySQLHelper import *
from downloader import Downloader
import lxml.html


SLEEP_TIME = 1
DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

# URL = 'http://gsxt.saic.gov.cn/'
db = MySQLHelper()
nm = 0

def threaded_crawler(delay=0, scrape_callback=None, user_agent=DEFAULT_AGENT, proxies=None, num_retries=3 ,max_threads=10 ,timeout=60, URL=None):
    '''                |            |                   |                        |                |             |              |
                       |            |                   |                        |                |             |              |_超时时间
                       |            |                   |                        |                |             |_进程中最大线程数
                       |            |                   |                        |                |_重试数
                       |            |                   |                        |_
                       |            |                   |_ 用户代理
                       |            |_ 回调函数
                       |_ 延迟
    '''
    crawl_queue = [URL]
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)
    images = Images()

    def _queue():
        while True:
            try:
                pic_url = crawl_queue.pop()
            except IndexError:
                break
            else:
                while True:
                    html = D(pic_url)
                    if html != '':
                        break

                string = MySQLdb.escape_string(html)  # 字符串转义
                sql = "insert into " + 'tianjing_images' + "(image_url,image_data) value('%s', '%s')" % (pic_url, string)
                db.insert(sql)  # 存入数据库
                crawl_queue.append(images.tianjing_images())
                '''
                #urls = []
                #country = []
                tree = lxml.html.fromstring(html)
                _as = tree.cssselect('div#wrap  ul.map  a')  # 得到a标签

                pic_name = str(uuid.uuid1()) + '.jpg'
                with open('pic1/' +pic_name, 'wb') as f:
                    f.write(html)
                '''

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads:
            thread = threading.Thread(target=_queue)
            thread.setDaemon(True)  # 守护线程
            thread.start()
            threads.append(thread)

        time.sleep(SLEEP_TIME)

def process_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    print '为 {} 核CPU'.format(num_cpus)
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == '__main__':


    p = Proxies_to_db()
    p.TO_DB(db)  #　把代理存入数据库里

    sql = 'select proxy_url from proxy'
    results = db.query(sql)    # 查找所有的代理

    proxies = [''.join(result) for result in results]  #　把元组转化为列表
    process_crawler(0, proxies=proxies, max_threads=10, timeout=10, URL='http://tjcredit.gov.cn/verifycode')

    db.close()

