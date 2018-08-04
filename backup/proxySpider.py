
import sys
import requests
from bs4 import BeautifulSoup

baseUrl = b'http://www.xicidaili.com/nn/'
publicUrl = b'119.29.94.38'

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

    return httpsProxies, httpProxies

#测试代理可用性
def proxyTest(IP, port, mode = 'https', timeout = 5):
    proxy = {mode: 'http://' + IP + ':' + port}
    try:
        if mode == 'https':
            r = requests.get(b'https://www.ip.cn/', proxies = proxy, timeout = 5).text
            soup = BeautifulSoup(r, 'lxml')
            foreignIP = soup.find('div', attrs = {'class': 'well'}).p.code.string
        else:
            r = requests.get(b'http://ip.chinaz.com/', proxies = proxy, timeout = 5).text
            soup = BeautifulSoup(r, 'lxml')
            foreignIP = soup.find('dd', attrs = {'class': 'fz24'}).string
    except:
        return False
    print(foreignIP)    
    if foreignIP == publicUrl:
        return False
    else:
        return True

if __name__ == '__main__':
    httpsProxy, httpProxy = get(1)
    
    print('https:')
    for p in httpsProxy:
        if(proxyTest(p[0], p[1], 'https')):
            print(p)

    print('http:')
    for p in httpProxy:
        if(proxyTest(p[0], p[1], 'http')):
            print(p)





