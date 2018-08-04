#!/home/ubuntu/env/spider/bin/python3

import sys
sys.path.append('./')


import proxyGetter.xiciProxyGetter as getter
import proxyVerify.proxyVerify as verify



if __name__ == '__main__':
    g = getter.xiciProxyGetter()
    counter = 1
    ver = verify.proxyVerify()
    proxies = g.get(500)
#    for i in proxies:
#        print(i)
    print('---------------------')
    ver.verifyMultiThreading(proxies, 300)
    
    print('--------------')

    



