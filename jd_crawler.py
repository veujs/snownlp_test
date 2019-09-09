import requests
from config import *
import re
import json
import math
from retrying import retry
from sql import jd_sql
import csv
# import pandas


class Jd_Comments(object):

    def __init__(self):
        self.req = Request()
        self.start_url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds=37245978364&callback=jQuery2257914&_=1567839796282"
        self.base_url = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1182&productId=37245978364&score=%s&sortType=5&page=%s" \
              "&pageSize=10&isShadowSku=0&fold=1"

        self.headers = {
            'Referer': 'https://item.jd.com/37245978364.html'
        }
        self.sql = jd_sql

    def get_num(self):
        proxies, headers = self.req.proxy(type2=0, headers=self.headers)
        response = requests.get(url=self.start_url, headers=headers, proxies=proxies)
        if response.status_code in [200, 201]:
            data = re.findall('jQuery2257914\((.*?)\);', response.text, re.S)[0]
            data_json = json.loads(data)
            CommentsCount = data_json.get('CommentsCount')[0]
            PoorCount = CommentsCount.get('PoorCount')
            GoodCount = CommentsCount.get('GoodCount')
            CommentCount = CommentsCount.get('CommentCount')
            return GoodCount, PoorCount, CommentCount
        else:
            print("获取好评数以及差评数失败！！")

    def create_urls(self, rank, num):
        urls = []
        for i in range(0, math.ceil(num/10)):
            url = self.base_url%(rank, i)
            print(url)
            urls.append(url)
        return urls

    @retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=2000)
    def spider_one(self, rank, url):
        proxies, headers = self.req.proxy(type2=0, headers=self.headers)
        response = requests.get(url=url, headers=headers, proxies=proxies)
        if response.status_code in [200, 201] and response.text:
            data = re.findall('fetchJSON_comment98vv1182\((.*?)\);', response.text, re.S)[0]
            data_json = json.loads(data)
            comments = data_json.get('comments')
            if comments:
                items = []
                for one in comments:
                    item = {}
                    item['good'] = '二手apple ' + one.get('referenceId')
                    item['content'] = one.get('content').replace('\n', '')
                    item['eval'] = rank
                    item['created_at'] = one.get('creationTime')
                    # 数据转存至mysql数据库中
                    # self.sql.insert_one(item)

                    # 数据保存到本地的csv文件中
                    self.save_to_csv(filename='jd_comments', item=item.values())
                    print(item)
                    if item:
                        items.append(item)
                return items
            else:
                return False

        else:
            print("访问失败！！")

    def spider_many(self):
        GoodCount, PoorCount, CommentCount = self.get_num()
        print(GoodCount, PoorCount, CommentCount)
        good_urls = self.create_urls(rank=3, num=GoodCount)
        for g_url in good_urls:
            result = self.spider_one(rank=3, url=g_url)
            if not result:
                break
        # print("111111111111111111111111111111111111111111111111111")
        poor_urls = self.create_urls(rank=1, num=PoorCount)
        page = 0
        for p_url in poor_urls:
            print('page: ', page)
            page += 1
            result = self.spider_one(rank=1, url=p_url)
            if not result:
                break

    def save_to_csv(self, filename=None, item=[]):
        name = '{}.csv'.format(filename)
        with open(name, 'a', encoding='utf-8-sig') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(item)
            # f_csv.writerows(rows)


if __name__ == '__main__':
    jd_comment = Jd_Comments()
    jd_comment.spider_many()




