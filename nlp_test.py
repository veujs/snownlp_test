import snownlp
from snownlp import SnowNLP

"""查看默认的编码类型"""
import sys
print(sys.stdout.encoding)


def isiter(obj=None):
    """迭代判断"""
    from collections import Iterable, Iterator
    # 例：
    fruit = {
        '苹果': '红色',
        '橘子': '黄色'
    }
    x = obj
    if not obj: obj = fruit
    y = lambda x: isinstance(x, Iterable)
    return y(obj)


s = SnowNLP('这个东西很惨')
tags = s.tags
pinyin = s.pinyin    # 转化为拼音
prob = s.sentiments  # positive的概率
sentense = s.sentences
keywords = s.keywords(10)
print("s.words: ", s.words)     # 分词
print("tags: ", list(tags))     # 词性标注
print("pinyin: ", pinyin)
print("prob: ", prob)           # 情感分词概率
print("sentense: ", sentense)   # 断句
print("keywords: ", keywords)   # 关键词提取

# text = '''
# 自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
# 它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
# 自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
# 因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
# 所以它与语言学的研究有着密切的联系，但又有重要的区别。
# 自然语言处理并不是一般地研究自然语言，
# 而在于研制能有效地实现自然语言通信的计算机系统，
# 特别是其中的软件系统。因而它是计算机科学的一部分。'''
#
# print(text)
# s = SnowNLP(text)
# keywords = s.keywords(3)
# summary = s.summary(3)
# sentence = s.sentences
# tags = s.tags
# pinyin = s.pinyin    # 转化为拼音
# prob = s.sentiments  # positive的概率
# print("s.words: ", s.words)
# print("tags: ", list(tags))
# print("pinyin: ", pinyin)
# print("prob: ", prob)
# print("keywords: ", keywords)
# print("summary: ", summary)
# print("sentence: ", sentence)

# import pandas as pd
# from pandas import Series, DataFrame
# import numpy as np
#
# if __name__ == '__main__':
#     df = pd.read_csv('jd_comments.csv',header=None)
#     print(df.head())

