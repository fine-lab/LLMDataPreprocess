import json
import os

# 合并去重
import numpy as np

path = "D://aData//JS代码生成//数据处理//去重后"
result_path = "D://aData//JS代码生成//数据处理//数据集合并去重"


# 合并去重
def dedup(p):
    name_files = os.listdir(p)  # 得到文件夹下的所有文件名称
    allconversation = set()
    result = []
    # dup = 0
    for file in name_files:
        # 获取json数据
        with open(p + "//" + file, 'r', encoding='utf-8') as f:
            rows = json.load(f)
        for row in rows:
            if not allconversation.__contains__(str(row.get("conversations"))):
                allconversation.add(str(row.get("conversations")))
                result.append(row)
        f.close()
    print(result.__len__())
    return result


# 重新分配存储
def redistri(p, result):
    # 训练集:测试集:验证集 = 8:1:1
    train = []
    test = []
    val = []
    len = result.__len__()
    for i in range(len):
        if i <= len / 10:
            test.append(result[i])
        elif len / 10 < i <= len / 5:
            val.append(result[i])
        else:
            train.append(result[i])
    # 训练集
    with open(p + "train(" + str(train.__len__()) + ").json", 'w', encoding='utf-8') as f:
        json.dump(train, f, ensure_ascii=False, indent=4)
    f.close()
    # 测试集
    with open(p + "test(" + str(test.__len__()) + ").json", 'w', encoding='utf-8') as f:
        json.dump(test, f, ensure_ascii=False, indent=4)
    f.close()
    # 验证集
    with open(p + "val(" + str(val.__len__()) + ").json", 'w', encoding='utf-8') as f:
        json.dump(val, f, ensure_ascii=False, indent=4)
    f.close()


def resorted(result, orig, target):
    result = sorted(result, key=lambda x: int(target.index(orig[int(x["id"])])))
    return result


def reindex(l):
    for i in range(len(l)):
        l[i]["id"] = str(i)
    return l


# 最终流程
def final(path_spec, orig, target):
    result = dedup(path + path_spec)
    result = reindex(result)
    result = resorted(result, orig, target)
    redistri(result_path + path_spec + "//", result)


name_result = dedup(path + "//数据集-(all_1102_pretty)(方法名称)")
name_result = reindex(name_result)
orig = name_result
name_result = list(np.random.permutation(name_result))
redistri(result_path + "//数据集-(all_1102_pretty)(方法名称)//", name_result)

final("//数据集-(all_1102_pretty)(方法搜索的关键字)//初始去重", orig, name_result)
# key_result = dedup(path + "//数据集-(all_1102_pretty)(方法搜索的关键字)//初始去重")
# key_result = reindex(key_result)
# key_result = resorted(key_result, orig, name_result)
# redistri(result_path + "//数据集-(all_1102_pretty)(方法搜索的关键字)//初始去重//", key_result)

final("//数据集-(all_1102_pretty)(方法的功能说明)", orig, name_result)
# describe_result = dedup(path + "//数据集-(all_1102_pretty)(方法的功能说明)")
# describe_result = reindex(describe_result)
# describe_result = resorted(describe_result, orig, name_result)
# redistri(result_path + "//数据集-(all_1102_pretty)(方法的功能说明)//", describe_result)

final("//数据集-(all_1102_pretty)(无注释)", orig, name_result)
# none_result = dedup(path + "//数据集-(all_1102_pretty)(无注释)")
# none_result = reindex(none_result)
# none_result = resorted(none_result, orig, name_result)
# redistri(result_path + "//数据集-(all_1102_pretty)(无注释)//", none_result)
