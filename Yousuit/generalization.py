from collections import OrderedDict

from faker import Faker
import random

import gene_area_module
import instruction


class YousuiteFakerDemo:
    # ["厨房", "麦当劳", "演唱会", "银行", "植物园", "视频网站", "霍格沃茨", "生物实验室", "图书馆"]
    unit_dict = {
        # "厨房": ["刀具", "烹饪器具", "餐具", "厨房电器", "储存容器", "烹饪调味料", "生鲜食材", "清洁用品"]
        "刀具": "把",
        "烹饪器具": "件",
        "餐具": "套",
        "厨房电器": "台",
        "储存容器": "个",
        "烹饪调味料": "瓶",
        "生鲜食材": "斤",
        "清洁用品": "瓶/包/支/罐",
        # "麦当劳": ["早安套餐", "儿童套餐", "学生套餐", "多人套餐"]
        "早安套餐": "份",
        "儿童套餐": "份",
        "学生套餐": "份",
        "多人套餐": "份",
        # "演唱会": ["看台区", "vip区"]
        "看台区": "座位数",
        "vip区": "座位数",
        # "银行": ["财务服务", "投资产品", "线上银行服务", "其他服务"]
        "财务服务": "用户数",
        "投资产品": "产品数",
        "线上银行服务": "用户数",
        "其他服务": "用户数",
        # "植物园": ["展示区", "教育区", "休闲区"]
        "展示区": "参观人数",
        "教育区": "参观人数",
        "休闲区": "参观人数",
        # "视频网站": ["电影", "电视剧", "综艺节目", "纪录片", "动画", "短片", "原创"]
        "电影": "票房",
        "电视剧": "收视率",
        "综艺节目": "订阅数",
        "纪录片": "订阅数",
        "动画": "订阅数",
        "短片": "部",
        "原创": "部",
        # "霍格沃茨": ["魔法书籍", "魔法工具", "学习用具", "魔法药剂", "魔法生物", "魔法装置", "特殊食物", "宿舍用品", "课堂设备", "运动器材"]
        "魔法书籍": "本",
        "魔法工具": "件",
        "学习用具": "件",
        "魔法药剂": "瓶",
        "魔法生物": "只",
        "魔法装置": "台",
        "特殊食物": "份",
        "宿舍用品": "套",
        "课堂设备": "台",
        "运动器材": "件",
        # "生物实验室": ["实验设备", "实验耗材", "安全设备", "实验文具"]
        "实验设备": "台",
        "实验耗材": "份",
        "安全设备": "件",
        "实验文具": "套",
        # "图书馆": ["图书", "期刊", "参考资料", "多媒体资料", "报纸", "地图和地理资料", "历史档案", "文献综述", "学位论文"]
        "图书": "册",
        "期刊": "本",
        "参考资料": "本",
        "多媒体资料": "张",
        "报纸": "份",
        "地图和地理资料": "张",
        "历史档案": "卷",
        "文献综述": "篇",
        "学位论文": "篇",
        # "医院": ["医疗设备", "药品", "医疗用品", "医护人员"]
        "医疗设备": "台",
        "药品": "种",
        "医疗用品": "件",
        "医护人员": "人",
    }
    def __init__(self):
        # 实例化时，如果要生成中国的数据信息，参数内要加上"zh-CN"
        self.fake = Faker("zh-CN")
        self.fake.add_provider(gene_area_module.MyProvider)

    def get_must(self, first_module_list, first_module):
        must = "必须购买"
        must_num = random.randint(1, 3)
        print(must_num)
        count = 0
        for i in range(must_num):
            must_first_module = self.fake.random_element(first_module_list)
            if must_first_module not in must and must_first_module != first_module:
                must += ("“" + must_first_module + "”，")
                count += 1
        if count == 0:
            must = ""
        else:
            must = must[:-1]  # 删除最后一个逗号，
        return must

    def yousuite(self, count):
        msg_formal = "ID,一级领域,二级领域,模块一级,模块二级,计量单位,收费类型,包含许可数,基础价格（元/年）,价格阶梯,单价（元/年）,购买约束,许可购买说明,特殊许可说明,特殊物料说明\n"
        # msg_formal = "ID,一级领域,二级领域,模块一级,模块二级,计量单位,收费类型,包含许可数,基础价格（元/年）,价格阶梯,单价（元/年）,购买约束,许可购买说明,特殊许可说明,特殊物料说明,城市,成本,备注词,公司名\n"
        num = 0
        first_module_list = set()  # 生成购买约束需要使用
        ins = instruction.Instruction()
        for i in range(count):
            # 领域&模块
            area_module = self.fake.area_module()
            first_area = area_module[0]
            second_area = area_module[1]
            first_module = area_module[2]
            first_module_list.add(first_module)
            second_module = area_module[3]
            # 计量单位
            unit = self.unit_dict[second_area]
            # 收费类型
            pay_type = self.fake.random_element(
                elements=OrderedDict([("定期收费", 0.4), ("一次性收费", 0.3), ("按使用量计费", 0.2), ("服务费用", 0.1)]))
            # 包含许可数
            permission_num = self.fake.random_element(elements=OrderedDict(
                [(random.randint(0, 10000), 0.7), ("", 0.3)]))
            # 基础价格（元/年）
            price_fundation = self.fake.random_element(elements=OrderedDict([
                (self.fake.pricetag().replace(",",""), 0.9), ("", 0.1)]))
            # 价格阶梯
            r1 = random.randint(1, 1001)
            r2 = random.randint(2, 10001)
            while r1 >= r2:
                r2 = random.randint(2, 10001)
            price_level = self.fake.random_element(elements=OrderedDict(
                [((str(r1) + '-' + str(r2)), 0.7), ("", 0.3)]))
            # price_level = self.fake.numerify(text="@%-@%#")
            # 单价（元 / 年）
            price_one = self.fake.random_element(elements=OrderedDict(
                [(self.fake.pricetag().replace(",", ""), 0.9), ("", 0.1)]))
            # 购买约束，保留 必须购买"xxx" 句式，使用“，”分隔
            must = self.get_must(first_module_list, first_module)
            constraint = self.fake.random_element(elements=OrderedDict(
                [(must, 0.7), ("", 0.3)]))
            # 许可购买说明
            # buy_permission = self.fake.random_element(elements=OrderedDict(
            #     [(self.fake.sentence(), 0.3), ("", 0.7)]))
            buy_permission = self.fake.random_element(elements=OrderedDict(
                [(ins.get_instruction(self.fake.word(), 1, random.randint(7, 20)), 0.3),
                 ("", 0.7)])).replace(" ", "")
            print(buy_permission)
            # 特殊许可说明
            special_permission = self.fake.random_element(elements=OrderedDict(
                [("功能许可", 0.4), ("区间许可", 0.2), ("定制许可", 0.2), ("用户许可", 0.1), ("", 0.1)]))
            # 特殊物料说明
            special_material = self.fake.random_element(elements=OrderedDict(
                [("限制销售地区", 0.35), ("限制购买数量", 0.15), ("授权销售", 0.25), ("预定制", 0.15), ("", 0.1)]))
            # 城市
            city = self.fake.city_name()
            # 成本
            cost = self.fake.pricetag().replace(",","")
            # 备注词, 公司名
            word = self.fake.word()
            # 公司名
            company = self.fake.company()
            # 全部信息
            new_msg = f"{first_area},{second_area},{first_module},{second_module},{unit},{pay_type},{permission_num},{price_fundation},{price_level},{price_one},{constraint},{buy_permission},{special_permission},{special_material}\n"
            # new_msg = f"{first_area},{second_area},{first_module},{second_module},{unit},{pay_type},{permission_num},{price_fundation},{price_level},{price_one},{constraint},{buy_permission},{special_permission},{special_material},{city},{cost},{word},{company}\n"
            print(new_msg)
            # 去重
            if new_msg not in msg_formal:
                num += 1
                msg_formal += (f"{num}," + new_msg)
        return msg_formal


if __name__ == '__main__':
    # 实例化FakeDemo对象
    f = YousuiteFakerDemo()
    # 生成10个人的信息(序号,姓名,电话,邮编)
    data = f.yousuite(200)
    # print(data)

    with open("data.csv", "w") as d:
        d.write(data)
    # f = Faker(["zh_CN"])
    # for i in range(10):
    #     print(f.address())