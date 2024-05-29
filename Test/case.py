import json

import tablib
import pandas as pd
import random

import util.excel_util as ex


def get_sample(df, path, num):
    data_list = ex.excel_to_listdict(df)
    header = list(df.columns)
    result = []
    for i in data_list:
        if i['acc'] == 0:
            result.append(i)
    result = random.sample(result, num)
    ex.list_to_excel(path + '236js_test_抽样.xlsx', header, result)


def get_bug_sum(df, path):
    data_list = ex.excel_to_listdict(df)
    data_dict = {}
    for i in data_list:
        s = i['difference'].split(';')
        for j in s:
            if j in data_dict.keys():
                data_dict[j] += 1
            else:
                data_dict[j] = 1
    header = list(['bug', 'num'])
    data = []
    for i in data_dict:
        body = []
        body.append(i)
        body.append(data_dict[i])
        data.append(tuple(body))
    data = tablib.Dataset(*data, headers=header)
    open(path + '统计.xlsx', 'wb').write(data.xls)


def check_leak(df, train):
    data_list = ex.excel_to_listdict(df)
    conversations = []  # 训练集conversations列表
    leak = []
    # for i in train:
    #     conversations.append(i['conversations'])
    for i in data_list:
        if i['acc'] == 1:
            prompt = json.loads(i['prompt'])
            conversation = [{'from': 'human', 'value': prompt[0]['content']},
                            {'from': 'gpt', 'value': i['gold']}]
            for j in train:
                if conversation == j['conversations']:
                    print(i)
                    print(j['id'])
                    leak.append(i)
    # print(leak)





path = "D:\\aData\\JS代码生成\\测试\\case分析\\第二次\\"
# 把Excel文件中的数据读入pandas
df = pd.read_excel(path + '236js_test_抽样.xlsx')
# get_bug_sum(df, path)
# get_sample(df, path, 50)
# train = open(path + 'train_fjbdy.json', 'r', encoding='utf-8')
# train = json.load(train)
check_leak(df, [])
