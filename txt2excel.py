import numpy as np
import xlrd
import xlwt
import os
import tablib
f = open('D:\\aData\\JS代码生成\\测试\\质量检测\\核心2_3.txt','r')  # 打开数据文本文档，注意编码格式的影响，这里用的是ANSI编码

header = ["File Name", "Issues", "Lines of Code", "Total Lines"]
data = []
for line in f:
    body = []
    info = line.split(' ') # txt文件中每行的内容按‘ ’分割并存入数组中
    for i in info:
        if not i == "":
            body.append(i.replace("\n", ""))
    data.append(tuple(body))
data = tablib.Dataset(*data,headers=header)
open('D:\\aData\\JS代码生成\\测试\\质量检测\\代码质量检测结果_核心2_3.xls', 'wb').write(data.xls)