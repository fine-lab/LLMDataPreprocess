import util.excel_util as ex

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import random


def draw_hist(data, title):
    num_list = []
    for i in data:
        num_list.append(i['插入代码'].count('\n') + 1)
    print(min(num_list), max(num_list))
    group_num = max(num_list) - min(num_list)
    plt.hist(num_list, bins=group_num, rwidth=0.8)
    plt.title(title, fontdict=dict(family='SimHei'))
    plt.xlabel('插入代码行数', fontdict=dict(family='SimHei'))
    plt.ylabel('数量', fontdict=dict(family='SimHei'))
    plt.show()


# 同一文件内最多取5条训练数据
def get_5data(data):
    # 将数据按照id划分
    id_list = {}
    for i in data:
        if i['id'] in id_list.keys():
            id_list[i['id']].append(i)
        else:
            id_list[i['id']] = [i]
    # 随机顺序
    for i in id_list.values():
        random.shuffle(i)
    # 取每个list前5条数据
    result = []
    for i in id_list.values():
        if len(i) > 5:
            result += i[:5]
        else:
            result += i
    return result


# 只对1行数据抽样调整占比-可以先用2000
def get_n_oneline(data, num):
    oneline_list = []  # 生成代码为1行的数据
    other_list = []  # 生成代码不为1行的数据
    for i in data:
        if i['插入代码'].count('\n') == 0:
            oneline_list.append(i)
        else:
            other_list.append(i)
    oneline_list = random.sample(oneline_list, num)
    result = oneline_list + other_list
    return result


path = "D:\\aData\\JS代码生成\\数据处理\\非脚本定义类\\数据集_非prompt\\"
df = pd.read_excel(path + '数据集_初始划分\\train(4666).xlsx')
# df = pd.read_excel(path + 'train(4020)_同一文件保留5条数据.xlsx')
# df = pd.read_excel(path + 'train(4586)_抽样2000条生成代码1行数据.xlsx')

data_list = ex.excel_to_listdict(df)
# draw_hist(data_list, '没有限制的数据')
# draw_hist(data_list, '同一文件保留5条数据')
# draw_hist(data_list, '抽样2000条生成代码1行数据')

header = list(df.columns)
# ex.list_to_excel(path + 'train_同一文件保留5条数据.xlsx', header, get_5data(data_list))
ex.list_to_excel(path + 'train_抽样1200条生成代码1行数据.xlsx', header, get_n_oneline(data_list, 1200))
