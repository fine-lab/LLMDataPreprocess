import math

import pandas as pd
import tablib


def excel_to_listdict(df):
    header = list(df.columns)
    list_dic = []  # excel转list嵌套dict
    for i in df.values:  # i 为每一行的value的列表
        a_line = dict(zip(header, i))
        list_dic.append(a_line)
    return list_dic


# 过滤去重
def filter_init():
    path = "D:\\aData\\JS代码生成\\测试\\质量检测\\"
    # 把Excel文件中的数据读入pandas
    df = pd.read_excel(path + '评分过滤\\代码质量检测结果.xls')

    list_dic = excel_to_listdict(df)

    data = []
    list_para = []  # 存储Issues + Lines o Code + Total Lines
    count = 0
    for rows in list_dic:
        body = []
        para = str(rows["Issues"]) + "-" + str(rows["Lines o Code"]) + "-" + str(rows["Total Lines"]) \
               + "-" + str(rows["脚本描述"])
        if list_para.__contains__(para) and isinstance(rows["脚本描述"], str):
            print(para)
        # 过滤
        # if not len(rows["Total Lines"]) == 1 and not rows["Total Lines"] == rows["Lines o Code"]:
        # 去重
        if not list_para.__contains__(para) and not len(rows["Total Lines"]) == 1 \
                and not rows["Total Lines"] == rows["Lines o Code"]:
            for row in rows.values():
                body.append(row)
            data.append(tuple(body))

        list_para.append(para)
    data = tablib.Dataset(*data, headers=list(df.columns))
    open(path + '评分过滤_后端脚本\\代码质量检测结果_过滤去重.xls', 'wb').write(data.xls)


def save_to_excel(file, header, result):
    data = []
    for rows in result:
        body = []
        for row in rows.values():
            body.append(row)
        data.append(tuple(body))
    data = tablib.Dataset(*data, headers=header)
    open(file, 'wb').write(data.xls)


# 按照api、workflow、rule分类
def filter_backend_type():
    path = "D:\\aData\\JS代码生成\\测试\\质量检测\\评分过滤_后端脚本\\"

    api_id = list(pd.read_excel(path + '原始数据分类\\API.xlsx')['id'])
    rule_id = list(pd.read_excel(path + '原始数据分类\\RULE.xlsx')['id'])
    workflow_id = list(pd.read_excel(path + '原始数据分类\\WORKFLOW.xlsx')['id'])

    df_filter = pd.read_excel(path + '过滤去重\\代码质量检测结果_过滤去重.xls')
    list_dic = excel_to_listdict(df_filter)
    header = list(df_filter.columns)

    # 按照api、rule、workflow对数据进行分类
    api = []
    rule = []
    workflow = []
    for i in list_dic:
        id = i["File Name"].replace(".js", "")
        if api_id.__contains__(id):
            api.append(i)
        elif rule_id.__contains__(id):
            rule.append(i)
        elif workflow_id.__contains__(id):
            workflow.append(i)

    save_to_excel(path + "API_过滤去重.xls", header, api)
    save_to_excel(path + "RULE_过滤去重.xls", header, rule)
    save_to_excel(path + "WORKFLOW_过滤去重.xls", header, workflow)


# filter_backend_type()
# filter_init()
