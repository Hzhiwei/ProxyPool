#!/usr/bin/python3

import pymysql
import time
import sys
import requests
from bs4 import BeautifulSoup

baseUrl = b'http://www.xicidaili.com/nn/'

#获取一页上的代理
def get(pageNum):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    html = requests.get(baseUrl + str(pageNum).encode(), headers = user_agent).text
    soup = BeautifulSoup(html, 'lxml')
    originList = soup.find('table', attrs = {'id': 'ip_list'}).tr.find_next_siblings()
    
    httpProxies = []
    httpsProxies = []

    for origin in originList:
        td = origin.find_all('td')
        ip = td[1].get_text()
        port = td[2].get_text()
        mode = td[5].get_text().lower()
        location = td[3].get_text().replace('\n', '')
        if mode == 'http':    
            httpProxies.append((ip, port, location))
        else:
            httpsProxies.append((ip, port, location))

    return httpProxies, httpsProxies

def proxyUsable(proxy, mode = 'https'):
    pass    

#过滤可用代理
def filterUsable(proxies, mode = 'https'):
    usableProxies = []
    for proxy in proxies:
        proxyData = {proxy[2].lower(): 'http://' + proxy[0] + ':1' + proxy[1]}
        try:
            r = requests.get('http://www.baidu.com', proxies = proxyData, timeout = 3)
            if r.status_code == 200:
                usableProxies.append(proxy)
        except:
            pass
    return usableProxies

#获取一个可用的代理
def getOneUsableProxy(num):
    while 1:
        proxies = get(num)
        for proxy in proxies:
            testProxy = filterUsable([proxy])
            if len(testProxy) == 0:
                continue
            else:
                yield testProxy[0]
        num += num

#获取ip
def getPublicIP(proxy = None):
    try:
        r = requests.get(b'http://ip.chinaz.com/', proxies = proxy, timeout = 5).text
        soup = BeautifulSoup(r, 'lxml')
        httpIP = soup.find('dd', attrs = {'class': 'fz24'}).string
    except:
        httpIP = '0.0.0.0'

    try:
        r = requests.get(b'https://www.ip.cn/', proxies = proxy, timeout = 5).text
        soup = BeautifulSoup(r, 'lxml')
        httpsIP = soup.find('div', attrs = {'class': 'well'}).p.code.string
    except:
        httpsIP = '0.0.0.0'

    return httpIP, httpsIP

if __name__ == '__main__':
#    proxies = []
#    if len(sys.argv) == 1:
#        proxies = filterUsable(get(1))
#        for proxy in proxies:
#            print(proxy)
#    else:
#        counter = 0
#        page = 1
#        itor = getOneUsableProxy(1)
#        for i in range(int(sys.argv[1])):
#            print(next(itor))

    db = pymysql.connect('localhost', 'proxy', 'proxy', 'proxy')
    cursor = db.cursor()
    num = int(sys.argv[1])
    proxies, https = get(1)
    for p in proxies:
        print(p)
        proxy = {p[2].lower(): 'http://' + p[0] + ':' + p[1]}
        if getPublicIP(proxy) != p[0] :
            print(p[2].lower() + 'http://' + p[0] + ':' + p[1])
            cursor.execute("INSERT INTO available (ip, port, time) VALUES (" + p[0] + "," + str(p[1]) + "," + "DATETIME()");
            db.commit()

