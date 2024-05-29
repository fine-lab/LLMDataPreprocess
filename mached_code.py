import json
import tablib
import os


# 获取列表id
def takeId(elem):
    return int(elem.get("id"))


# 数据清洗
def data_clean_name_key(name_matched, key_matched):
    # name中有，key中无，跳过不处理
    # name和key中都有，删除一半
    name_result = []
    key_result = []

    for k, v in name_matched.items():
        # 有多个方法名和关键字
        if key_matched.__contains__(k):
            name_matched[k].sort(key=takeId, reverse=False)
            key_matched[k].sort(key=takeId, reverse=False)
            # 偶数对半分，奇数方法名的多一个
            for i in range(len(name_matched.get(k))):
                if i < len(name_matched.get(k)) / 2:
                    name_result.append(name_matched.get(k)[i])
                else:
                    key_result.append(name_matched.get(k)[i])
        # 只有方法名
        else:
            name_result += name_matched[k]
    print(len(name_result))
    print(len(key_result))
    with open('D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法名称)//tarin('
              + str(len(name_result)) + ')_二次去重_无功能说明.json', 'w', encoding='utf-8') as f1:
        json.dump(name_result, f1, ensure_ascii=False, indent=4)
    f1.close()
    with open('D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法搜索的关键字)//tarin('
              + str(len(key_result)) + ')_二次去重_无功能说明.json', 'w', encoding='utf-8') as f2:
        json.dump(key_result, f2, ensure_ascii=False, indent=4)
    f2.close()


def data_clean_name_key_describe(name_matched, key_matched, describe_matched):
    # name中有，key和des中无，跳过不处理
    # name和key中有 or name和des中有，个一半
    # name key des中都有，三分之一分
    name_result = []
    key_result = []
    describe_result = []

    for k, v in name_matched.items():
        # 有name key 无des
        length = len(name_matched.get(k))
        if key_matched.__contains__(k) and not describe_matched.__contains__(k):
            name_matched[k].sort(key=takeId, reverse=False)
            key_matched[k].sort(key=takeId, reverse=False)
            # 偶数对半分，奇数方法名的多一个
            for i in range(length):
                if i < length / 2:
                    name_result.append(name_matched.get(k)[i])
                else:
                    key_result.append(name_matched.get(k)[i])
        # 有name des 无key
        elif not key_matched.__contains__(k) and describe_matched.__contains__(k):
            name_matched[k].sort(key=takeId, reverse=False)
            describe_matched[k].sort(key=takeId, reverse=False)
            # 偶数对半分，奇数方法名的多一个
            for i in range(length):
                if i < length / 2:
                    name_result.append(name_matched.get(k)[i])
                else:
                    describe_result.append(name_matched.get(k)[i])
        # 都有
        elif key_matched.__contains__(k) and describe_matched.__contains__(k):
            name_matched[k].sort(key=takeId, reverse=False)
            key_matched[k].sort(key=takeId, reverse=False)
            describe_matched[k].sort(key=takeId, reverse=False)
            for i in range(length):
                if i < length / 3:
                    name_result.append(name_matched.get(k)[i])
                elif length / 3 <= i < length * 2 / 3:
                    key_result.append(name_matched.get(k)[i])
                else:
                    describe_result.append(name_matched.get(k)[i])
        # 只有方法名
        else:
            name_result += name_matched[k]
    print(len(name_result))
    print(len(key_result))
    print(len(describe_result))
    with open('D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法名称)//tarin('
              + str(len(name_result)) + ')_二次去重.json', 'w', encoding='utf-8') as f1:
        json.dump(name_result, f1, ensure_ascii=False, indent=4)
    f1.close()
    with open('D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法搜索的关键字)//tarin('
              + str(len(key_result)) + ')_二次去重.json', 'w', encoding='utf-8') as f2:
        json.dump(key_result, f2, ensure_ascii=False, indent=4)
    f2.close()
    with open('D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法的功能说明)//tarin('
              + str(len(describe_result)) + ')_二次去重.json', 'w', encoding='utf-8') as f3:
        json.dump(describe_result, f3, ensure_ascii=False, indent=4)
    f3.close()


# 方法名统计
def name_process(matched_code):
    name_matched = {}
    with open("D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法名称)//train(314).json",
              'r', encoding='utf-8') as f2:
        name_rows = json.load(f2)
    for row in name_rows:
        c = 0
        s = ""
        for k, v in matched_code.items():
            # 计数
            if v.__contains__(row.get("conversations")[1].get("value")):
                # if v.__contains__(row.get("conversations")):
                if name_matched.__contains__(k):
                    name_matched[k].append(row)
                else:
                    name_matched[k] = [row]
                # 计算匹配次数
                c += 1
                s += k
        # 重复匹配
        # if c > 1:
        #     print(row)
        #     print(s)
    # 去重（特殊处理）
    name_matched["vicuna_39.json"] = name_matched.get("vicuna_39.json")[0:7]
    name_matched["vicuna_56.json"] = name_matched.get("vicuna_56.json")[7: 13] + [name_matched.get("vicuna_56.json")[4]]
    # print(sum(len(i) for i in name_matched.values()))
    return name_matched


def key_process(matched_code):
    # 关键字统计
    key_matched = {}
    temp = []  # 未匹配成功的数据
    with open(
            "D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法搜索的关键字)//关键字去重//train(201).json",
            'r', encoding='utf-8') as f3:
        key_rows = json.load(f3)
    for row in key_rows:
        c = 0
        if row.get("id") == "0":
            print()
        for k, v in matched_code.items():
            # 计数
            if v.__contains__(row.get("conversations")[1].get("value")):
                # if v.__contains__(row.get("conversations")):
                if key_matched.__contains__(k):
                    key_matched[k].append(row)
                else:
                    key_matched[k] = [row]
                # break
                c += 1
        # 匹配缺失
        if c == 0:
            temp.append(row)

    # 添加匹配缺失数据
    # print(sum(len(i) for i in key_matched.values()))
    return key_matched


def describe_process(matched_code):
    # 功能说明统计
    describe_matched = {}
    temp = []  # 未匹配成功的数据
    with open(
            "D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法的功能说明)//功能说明去重//train(177).json",
            'r', encoding='utf-8') as f4:
        describe_rows = json.load(f4)
    for row in describe_rows:
        c = 0
        for k, v in matched_code.items():
            # 计数
            if v.__contains__(row.get("conversations")[1].get("value")):
                # if v.__contains__(row.get("conversations")):
                if describe_matched.__contains__(k):
                    describe_matched[k].append(row)
                else:
                    describe_matched[k] = [row]
                # break
                c += 1
        # 匹配缺失
        # if c == 0:
        #     temp.append(row)
        #     print(row)
        # if c > 1:
        #     print(row)
    # print(sum(len(i) for i in describe_matched.values()))
    return describe_matched


path = "D://aData//JS代码生成//数据处理//脚本定义数据集-对应关系(方法名称)未划分"
files = os.listdir(path)  # 得到文件夹下的所有文件名称
# 循环里面的字典，将value作为数据写入进去
matched_code = {}
for file in files:  # 遍历文件夹
    with open(path + "//" + file, 'r', encoding='utf-8') as f1:
        rows = json.load(f1)
    value = []
    for row in rows:
        value.append(row.get("conversations")[1].get("value"))
        # value.append(row.get("conversations"))
    matched_code[file] = value
    f1.close()

des = describe_process(matched_code)
key = key_process(matched_code)
name = name_process(matched_code)
# data_clean_name_key_describe(name, key, des)
data_clean_name_key(name, key)