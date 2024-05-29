import util.excel_util as ex
import util.txt_util as txt

import pandas as pd
import random


def delete25(data):
    """
    删除代码行数大于25的数据
    :param data: excel转llist[dict]
    :return: 删除后结果
    """
    result = []
    count = 0
    for i in data:
        if i['插入代码'].count('\n') <= 25-1:
            result.append(i)
        else:
            count += 1
    print(count)

    return result


def get_type(data):
    """
    按照W R A划分数据集id
    :param data: excel转llist[dict]
    :return: W R A id的list
    """
    workflow = set()
    api = set()
    rule = set()
    for i in data:
        data_type = i['脚本类型']
        if data_type == 'WORKFLOW':
            workflow.add(i['id'])
        elif data_type == 'API':
            api.add(i['id'])
        else:
            rule.add(i['id'])
    return list(workflow), list(api), list(rule)


def distribution(data):
    """
    按照8:1:1划分训练集、测试集、验证集
    :param data: list[id]
    :return: 训练集、测试集、验证集 list[id]
    """
    random.shuffle(data)
    train = []
    test = []
    val = []
    length = len(data)
    for i in range(length):
        if i < length / 10:
            test.append(data[i])
        elif i < length / 5:
            val.append(data[i])
        else:
            train.append(data[i])
    return train, test, val


def get_data_by_id(data_id, data):
    """
    根据id将添加数据
    :param data_id: list[id]
    :param data: 数据总集
    :return: id在data_id中的数据
    """
    result = []
    for i in data:
        if i['id'] in data_id:
            result.append(i)
    return result


def get_dataset(data_list, path):
    """
    数据集分类划分训练集 总流程
    :param data_list:list[dict]
    :param path:文件路径
    """
    # 三个类型WORKFLOW、API、RULE内部id按8:1:1的比例划分训练、验证、测试集
    workflow_id, api_id, rule_id = get_type(data_list)
    train_w, test_w, val_w = distribution(workflow_id)  # workflow
    train_a, test_a, val_a = distribution(api_id)  # api
    train_r, test_r, val_r = distribution(rule_id)  # rule
    train_id = train_r + train_a + train_w
    test_id = test_r + test_w + test_a
    val_id = val_r + val_a + val_w

    # 获取训练测试验证集数据
    train = get_data_by_id(train_id, data_list)
    test = get_data_by_id(test_id, data_list)
    val = get_data_by_id(val_id, data_list)

    # 输出
    # id存储
    txt.list_to_txt(path + '数据集_非prompt\\数据集_初始划分\\train_id(' + str(len(train_id)) + ').txt', train_id)
    txt.list_to_txt(path + '数据集_非prompt\\数据集_初始划分\\test_id(' + str(len(test_id)) + ').txt', test_id)
    txt.list_to_txt(path + '数据集_非prompt\\数据集_初始划分\\val_id(' + str(len(val_id)) + ').txt', val_id)
    # 数据存储
    header = []  # excel表头
    for i in test[0].keys():
        header.append(i)
    ex.list_to_excel(path + '数据集_非prompt\\数据集_初始划分\\train(' + str(len(train)) + ').xlsx', header, train)
    ex.list_to_excel(path + '数据集_非prompt\\数据集_初始划分\\test(' + str(len(test)) + ').xlsx', header, test)
    ex.list_to_excel(path + '数据集_非prompt\\数据集_初始划分\\val(' + str(len(val)) + ').xlsx', header, val)


def get_dataset_by_id(data_list, path):
    """
    按照已划分训练集的文件id，划分对应id的数据
    :param data_list:list[dict]
    :param path:文件路径
    """
    # 直接通过文件获取
    train_id = txt.txt_to_list(path + '数据集_未标准化\\数据集_初始划分\\train_id(1306).txt')
    test_id = txt.txt_to_list(path + '数据集_未标准化\\数据集_初始划分\\test_id(165).txt')
    val_id = txt.txt_to_list(path + '数据集_未标准化\\数据集_初始划分\\val_id(163).txt')

    # id文件中不包含的id
    id_list_new = []
    for i in data_list:
        if not i['id'] in train_id and not i['id'] in test_id and not i['id'] in val_id:
            id_list_new.append(i)

    # 三个类型WORKFLOW、API、RULE内部id按8:1:1的比例划分训练、验证、测试集
    workflow_id, api_id, rule_id = get_type(id_list_new)
    train_w, test_w, val_w = distribution(workflow_id)  # workflow
    train_a, test_a, val_a = distribution(api_id)  # api
    train_r, test_r, val_r = distribution(rule_id)  # rule

    train_id += train_r + train_a + train_w
    test_id += test_r + test_w + test_a
    val_id += val_r + val_a + val_w

    # 获取训练测试验证集数据
    train = get_data_by_id(train_id, data_list)
    test = get_data_by_id(test_id, data_list)
    val = get_data_by_id(val_id, data_list)

    # 输出
    # id存储
    txt.list_to_txt(path + '数据集_非prompt\\数据集_初始划分\\train_id(' + str(len(train_id)) + ').txt', train_id)
    txt.list_to_txt(path + '数据集_非prompt\\数据集_初始划分\\test_id(' + str(len(test_id)) + ').txt', test_id)
    txt.list_to_txt(path + '数据集_非prompt\\数据集_初始划分\\val_id(' + str(len(val_id)) + ').txt', val_id)
    # 数据存储
    header = []  # excel表头
    for i in test[0].keys():
        header.append(i)
    ex.list_to_excel(path + '数据集_非prompt\\数据集_初始划分\\train(' + str(len(train)) + ').xlsx', header, train)
    ex.list_to_excel(path + '数据集_非prompt\\数据集_初始划分\\test(' + str(len(test)) + ').xlsx', header, test)
    ex.list_to_excel(path + '数据集_非prompt\\数据集_初始划分\\val(' + str(len(val)) + ').xlsx', header, val)


path = "D:\\aData\\JS代码生成\\数据处理\\非脚本定义类\\"
# 把Excel文件中的数据读入pandas
df = pd.read_excel(path + '鑫超切完的基于w2v去重的生数据20240105.xlsx')

data_list = ex.excel_to_listdict(df)
data_list = delete25(data_list)

get_dataset(data_list, path)