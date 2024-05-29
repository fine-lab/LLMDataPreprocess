import json

# 比较allinfo
allinfoPath = "D://aData//JS代码生成//数据处理//脚本定义数据优化20231211//匹配结果_脚本1_核心1"
with open(allinfoPath + "//result_56_AllInfo.json", 'r', encoding='utf-8') as f1:
    row1 = json.load(f1)
with open(allinfoPath + "//result_39_AllInfo.json", 'r', encoding='utf-8') as f2:
    row2 = json.load(f2)
print(row1 == row2)

# 比较vicana
allinfoPath = "D://aData//JS代码生成//数据处理//脚本定义数据集-对应关系(方法名称)未划分"
with open(allinfoPath + "//vicuna_56.json", 'r', encoding='utf-8') as f1:
    row1 = json.load(f1)
with open(allinfoPath + "//vicuna_39.json", 'r', encoding='utf-8') as f2:
    row2 = json.load(f2)
for i in range(len(row1)):
    if not row1[i] == row2[i]:
        print(row1[i])
        print(row2[i])
print(row1 == row2)