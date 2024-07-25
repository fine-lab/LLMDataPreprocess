from util.json_util import read_jsonl, dict2json
import re
import ast

org_content = read_jsonl(r'D:\aData\SFT\人力资源指令进化结果\晚如的任务——筛选合格的output\Qwen1.5-110B-Chat_SQL.jsonl')
new_content = []
for c in org_content:
    flag = True
    # output字段中，若含有类似‘SQL查询结果’的字符串，直接判定为不合格
    if 'SQL查询' in c['output'] or 'SQL执行' in c['output']:
        continue
    new_c = {}
    sql_filter = re.findall(r'\nSQL执行结果：(.*?)\n回答：', c['prompt'])[2]
    # SQL执行结果里面，如果有类似‘总计’、‘合计’的，这些数据你先看一下问题怎么问的，如果不合适就把‘总计’、‘合计’这种去掉
    if '总计' in sql_filter or '合计' in sql_filter:
        continue
    sql_result = ast.literal_eval(sql_filter)  # tuple list格式
    # sql = sql_filter.replace("'", "").replace(r"[(", "").replace(r")]", "").replace("), (", " ").replace(",", "")
    # sql_list = sql.split(" ")  # 便于比较
    for l in sql_result:
        for t in l:
            if str(t) not in c['output']:
                flag = False
                break
    if flag is False:
        continue
    new_c['id'] = c['id']
    new_c['instruction'] = c['instruction']
    new_c['input'] = c['input']
    new_c['output'] = c['output']
    new_c['SQL执行结果'] = sql_result
    new_c['source'] = c['source']
    new_c['datetime'] = c['datetime']
    new_content.append(new_c)
    print(sql_result)
dict2json("D:\\aData\SFT\人力资源指令进化结果\晚如的任务——筛选合格的output\\", new_content)
