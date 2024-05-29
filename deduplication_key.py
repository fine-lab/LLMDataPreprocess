import json
import os
import pandas as pd

# 获取列表id
def takeId(elem):
    return int(elem.get("id"))

# 获取重复关键词
dup = set()
data_frame=pd.read_excel('D://aData//JS代码生成//数据处理//dup_key.xls',sheet_name='Sheet1')
for i in data_frame.values:
    if i[1] == 1 or i[2] == 1:
        dup.add(i[0])

path = "D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法搜索的关键字)//初始去重"
files= os.listdir(path) # 得到文件夹下的所有文件名称

for file in files:
    result = []
    # 获取json数据
    with open(path + "//" + file, 'r', encoding='utf-8') as f:
        rows = json.load(f)
    for row in rows:
        flag = True # 是否重复，重复false，不重复true
        # 是否包含重复关键字
        for s in dup:
            if str(row.get("conversations")).__contains__("// " + s + r"\n"):
                flag = False
                # print("// " + s + r"\n")
                # print(row.get("id"))
                break
        if flag:
            result.append(row)
    #result.sort(key=takeId, reverse=False)
    f.close()

    with open('D://aData//JS代码生成//数据处理//数据集合并去重//数据集-(all_1102_pretty)(方法搜索的关键字)//关键字去重//' + file, 'w', encoding='utf-8') as f2:
        json.dump(result, f2, ensure_ascii=False, indent=4)
    f2.close()
    print(file + " ")
    print(result.__len__())

