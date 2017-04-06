# -*- coding:utf-8 -*-
# E:/PycharmProjects/
# create by boxiao on 2016/12/19
import multiprocessing
import threading

import time
import uuid

from downloader import Downloader

url = 'http://aic.hainan.gov.cn:1888/validateCode.jspx?type=1&id=0.3266812554981726'

SLEEP_TIME = 1
DEFAULT_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

# URL = 'http://gsxt.saic.gov.cn/'
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

    def _queue():
        while True:
            try:
                pic_url = crawl_queue.pop()
            except IndexError:
                break
            else:

                html = D(pic_url)
                pic_name = str(uuid.uuid1()) + '.png'
                with open('pic1/' +pic_name, 'wb') as f:
                    f.write(html)

                crawl_queue.append(url)

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

    process_crawler(0, proxies='', max_threads=10, timeout=10, URL=url)


