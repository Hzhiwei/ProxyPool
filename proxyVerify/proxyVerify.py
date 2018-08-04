#!/usr/bin/python3

import requests
import threading
import queue
import time
from widget.ThreadPool import ThreadPool

class proxyVerify(object):
    def __init__(self):
        self.count = 0

    def verifyOne(self, proxy, timeout = 5):
        _head = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        def verifyHttp(p):
            proxyArg = {'http':'http://' + str(proxy[0]) + ':' + str(proxy[1])}
            try:
                r = requests.get('http://www.qq.com/', proxies = proxyArg, headers = _head, timeout = timeout)
                return r.elapsed.total_seconds()
            except:
                return -1
        def verifyHttps(p):
            proxyArg = {'https':'https://' + str(proxy[0]) + ':' + str(proxy[1])}
            try:
                r = requests.get('https://www.baidu.com/', proxies = proxyArg, headers = _head, timeout = timeout)
                return r.elapsed.total_seconds()
            except:
                return -1
        proxyMap = {'http': verifyHttp, 'https': verifyHttps}
        return proxyMap[proxy[2]](proxy)
    
    def verifyAndWrite(self, proxy):
        r = self.verifyOne(proxy)
        if r != -1:
            self.count += 1
            print(self.count, end = ': ')
            print(proxy, end = ' ')
            print(r)

    def verifyMultiThreading(self, proxies, thread_num = 5, timeout = 5):
        pool = ThreadPool(thread_num)
        for i in proxies:
            pool.put(self.verifyAndWrite, ([i],{}))
        pool.wait()
        pool.terminal()


