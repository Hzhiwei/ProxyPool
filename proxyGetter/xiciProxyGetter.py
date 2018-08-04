# coding: utf-8


import requests
from .ProxyGetter import ProxyGetter
from lxml import etree

class xiciProxyGetter(ProxyGetter):
    def __init__(self):
        pass

    def get(self, num):
        urlHead = b'http://www.xicidaili.com/nn/'
        httpHead = {'User-agent': 'Mozilla/5.0'}
        counter = 1
        pageNum = 1
        proxyList = []
        while 1:
            try:
                html = requests.get(urlHead + str(pageNum).encode(), headers = httpHead).text
            except Exception as e:
                raise Exception("get data error!")
            
            et = etree.HTML(html)
            opList = et.xpath('//tr[@class]')
            for op in opList:
                ip = str(op.xpath('./td[2]')[0].text)
                port = int(str(op.xpath('./td[3]')[0].text))
                protocol = str(op.xpath('./td[6]')[0].text).lower()
                
                proxyList.append((ip, port, protocol))

                if counter >= num:
                    break
                counter = counter + 1
            if counter >= num:
                break
            pageNum = pageNum + 1
        return proxyList

if __name__ == '__main__':
    getter = xiciProxyGetter()
    counter = 1
    for p in getter.get(2000):
        print(counter, end = '')
        counter = counter + 1
        print(': ', end = '')
        print(p)

