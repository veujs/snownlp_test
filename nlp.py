import snownlp
from snownlp import SnowNLP
import pandas as pd
from snownlp import sentiment
import os
import random

current_path = os.getcwd()
df_train = pd.read_csv('jd_comments.csv', header=None)


def set_train_txt(origin_data):
    origin_data = pd.read_csv('jd_comments.csv', header=None)
    origin_data[df_train[2] == 3].iloc[:, 1].to_csv('pos.txt', sep='\t', index=False)
    origin_data[df_train[2] == 1].iloc[:, 1].to_csv('neg.txt', sep='\t', index=False)


def train_model(neg_path, pos_path):
    neg_path = os.path.abspath(os.path.join(os.getcwd(), 'neg.txt'))
    pos_path = os.path.abspath(os.path.join(os.getcwd(), 'pos.txt'))
    mod_path = os.path.abspath(os.path.join(os.getcwd(), 'sentiment.marshal'))
    sentiment.train(neg_path, pos_path)
    sentiment.save(mod_path)
    return mod_path


if __name__ == '__main__':
    # 1 数据收集 执行一次即可
    # df_train = pd.read_csv('jd_comments.csv', header=None)
    # df_train[df_train[2] == 3].iloc[:, 1].to_csv('pos.txt', sep='\t', index=False)
    # df_train[df_train[2] == 1].iloc[:, 1].to_csv('neg.txt', sep='\t', index=False)

    # 2 训练
    # neg_path = os.path.abspath(os.path.join(os.getcwd(), 'neg.txt'))
    # pos_path = os.path.abspath(os.path.join(os.getcwd(), 'pos.txt'))
    # mod_path = os.path.abspath(os.path.join(os.getcwd(), 'sentiment.marshal'))
    # print(mod_path)
    # sentiment.train(neg_path, pos_path)
    # sentiment.save(mod_path)

    # print(pos_path)

    # 3 随机测试
    # rand = random.randint(0, df_train.shape[0])
    # print(list(df_train.iloc[rand]))
    #
    # df_test_text = df_train.iloc[rand, 1]
    # s = SnowNLP(df_test_text)
    # print(s.sentiments)
    # print(df_train.shape[0])

    # 4 拿训练集集进行测试 识别准确率
    prob_list = []
    for i in range(0, df_train.shape[0]):
        s = SnowNLP(df_train.iloc[i, 1])
        prob = round(s.sentiments)
        prob_list.append(prob)
        # print(type(s.sentiments))
    df_train[df_train.shape[1]] = prob_list
    columns = ['good', 'content', 'eval', 'created_at', 'prob']
    df_train.columns = columns

    df_train_result = df_train.loc[:, ['content', 'eval', 'prob']]
    df_train_result['eval'] = df_train_result['eval'].map({3: 1, 1: 0})
    accurate = df_train_result[df_train_result['eval'] == df_train_result['prob']].shape[0] / df_train_result.shape[0]
    # df_train_result.to_csv('new_result.csv', index=False)
    # print('使用 新 model 识别准确率为：', accurate)

    df_train_result.to_csv('origin_result.csv', index=False)
    print('使用 原始model 识别准确率为：', accurate)
