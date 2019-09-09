import random
import time
import requests
from retrying import retry


class Request(object):

    @retry(stop_max_attempt_number=3)
    def get(self, url, user_type):
        # print(url,user_type)
        proxies, headers = self.proxy(user_type)
        response = requests.get(url, headers=headers, timeout=5, proxies=proxies)
        # print('状态吗', response.status_code)
        if response.status_code in [200]:
            return response
        # else:
        #     time.sleep(5)
        #     return self.get(url,  user_type)

    def proxy(self, type2, headers={}):

        proxies = {'http': 'http://proxy.tongmingmedia.com:4000/',
                   'https': 'http://proxy.tongmingmedia.com:4000/'

                   }

        if type2 == 1:
            # 手机端user-agent
            user_agent = [
                'Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.7.0.953 Mobile Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                'Mozilla/5.0 (iPhone 92; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.7.2 Mobile/14F89 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A372 MicroMessenger/6.5.15 NetType/4G Language/zh_CN',
                'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; SM-G9550 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.8 Mobile Safari/537.36',
            ]
        else:
            # 设置电脑端useragent
            user_agent = [
                # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                # 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
                # 'Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1',
                # 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
                # 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0',
                'Mozilla/5.0'
            ]

        headers['User-Agent']=random.choice(user_agent)

        return proxies, headers
