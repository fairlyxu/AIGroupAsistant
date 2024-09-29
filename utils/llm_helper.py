# -*-coding:utf-8 -*-

"""
# File       : llm_helper.py.py
# Time       ：2024/9/29 11:46
# Author     ：fairyxu 
# Description：
"""

import requests
import time
import json


def get_prompt(groups=[],regroup=[],group_num=7):
    groups = [('1', '云服务', '亲子、AI、哲学',
               '人工智能/培训/企业服务公司】丽台科技-英伟达GPU总代，冰特科技-自建算力平台，冰特算力学院-AI培训，英伟达深度学习中心-高中研学，元起点-灵活用工和知识产权',
               '1', '云服务组'),
              ('3', '硬件 / 半导体', 'AI在IT服务中的应用', '网络安全行业技术人员', '3', '硬件/半导体组'),
              ('4', '制造业/趋势发展', '无', '大家电业务负责人', '4', '制造业组'),
              ('5', '医疗健康和生命科学', 'AI在营销中的应用', '从医疗设备和耗材销售管理多年', '5',
               '医疗健康和生命科学组'),
              ('6', '医疗健康和生命科学', 'NIVIDA是否有在AI软件方面的布局考量，会在哪些领域做准备', '连续创业者', '5',
               '医疗健康和生命科学组'),
              ('7', '云服务', 'AI可能的发展趋势', '互联网从业者，现在做数字化转型相关工作', '1', '云服务组'),
              ('8', '硬件/半导体', '中国AI大算力芯片设计公司的前途和出路',
               '深耕半导体行业28年，负责苹果供应链16年，复旦大学EMBA，华东师范大学CTO学院产业导师', '3', '硬件/半导体组'),
              ('9', '医疗健康和生命科学', '数字人医护', 'AI医疗科技公司，主要做医学服务', '5', '医疗健康和生命科学组'),
              ('10', '医疗健康和生命科学', '无', '22级1班陈伊君', '5', '医疗健康和生命科学组'),
              ('11', '建筑 / 工程 / 交通运输', '想多了解元宇宙及AI计算目前的商用情况',
               '企业服务公司，服务内容设计咨询、数字化转型及工业智能制造', '6', '建筑/工程/交通运输组'),
              ('12', '智慧城市/空间', '英伟达芯片在智能分析领域的应用案例及未来规划',
               '华启智能科技副总经理，分管技术中心', '7', '智慧城市/空间组'),
              ('13', '建筑/工程/交通运输', 'AI为工程咨询带来怎样的便捷和行业的改变',
               '2022级1班17A，一家工程咨询公司的经营人', '6', '建筑/工程/交通运输组')]

    regroup = [('用户28', '硬件/半导体', '了解AI在应用的趋势', '10年创业老板  虔诚学习'),
               ('用户29', '制造业', '元宇宙在制造业的应用', '工学博士，长期从事测试技术与仪器开发')]

    groups_strings = '\n'.join(['|'.join(map(str, row)) for row in groups])
    regroup_strings = '\n'.join(['|'.join(map(str, row)) for row in regroup])
    prompt = """ 
        # Role
        资深企业培训师，对学生分组信息提取
        ## Skills
        - 精通中文
        - 能够理解文本
        ## Action
        你现在是企业管理咨询培训师，开展一场培训，对学生进行分组，最多分成%d组。 现在已经有%d位学生已经分好组。新加入了%d位学生需要分组，注意不要更改原来的分组结果，只针对新加入的同学进行分组
        根据每个学生提交的自我介绍和需要了解的问题进行相同领域分组，可以接受分组人数上的不平衡，尽可能分成相关领域为同一组，分组结束后提取出用户id：分组id:分组名称,并以JSON格式输出。
        原分组,每一行数据表示(用户编号｜行业｜兴趣的话题｜自我介绍|分组号｜分组名称):\n%s\n 
        新加入的同学信息，每一行数据表示(用户编号｜行业｜兴趣的话题｜自我介绍):\n%s 
        ## Constrains
        - 忽略无关内容 
        - 综合考虑用户行业和兴趣的话题以及自我介绍的内容
        - 必须保证你的结果只包含一个合法的JSON格式,用list存储结果
        ## Format
        - 对应JSON的key为：user_id, group_id, group_name
        """%(group_num,len(groups),len(regroup),groups_strings,regroup_strings)
    return prompt


#zhizengzeng
def llm_chat_zhizengzeng(groups=[],regroup=[],group_num=7):
    result = []
    prompt = get_prompt(groups,regroup)
    url="https://api.zhizengzeng.com/v1/chat/completions"
    api_secret_key = 'd60ca8832a0297ff3861136b649f3aa8';  # 你的api_secret_key
    headers = {'Content-Type': 'application/json', 'Accept':'application/json',
               'Authorization': "Bearer "+api_secret_key}
    params = {'user':'Tom',
               "model": "gpt-4o",
               "temperature": 0.7,
              'messages':[{'role':'assistant', 'content':prompt}]};
    response = requests.post(url, json.dumps(params), headers=headers)
    res = response.json()

    if res['code'] == 0 and res['msg']=='ok':
        datas = res['choices'][0]['message']['content']
        res = json.loads(datas)
        for k,v in res.items():
            result.append(v)

    return result


def llm_chat_tran(groups=[],regroup=[]):

    t1 = time.time()
    result = [{'user_id': 28, 'group_id': 3, 'group_name': '硬件/半导体组'}, {'user_id': 29, 'group_id': 4, 'group_name': '制造业组'}]
    prompt = get_prompt(groups,regroup)

    text = """根据每个学生提交的自我介绍和需要了解的问题进行相同领域和兴趣分组,现在对新加入的同学进行重新分组："""
    url = "http://test-content-api.shalltry.com/llm/chat"
    headers = {
        "api-key": "30JgICd.huKyNlifkfglPOSDpsBNozTc",
        "Content-Type": "application/json"
    }
    data = {
        "businessId": "7",
        "prompt": prompt,
        "model": "gpt-4o",
        "text": text,
        "maxTokens": 2000,
        "temperature": 0.7,
        "modelProvider": "azure"
    }
    """ """
    response = requests.post(url, headers=headers, json=data)
    res = response.json()
    print(res,type(res))
    if res['code'] == 200:
        datas = res['data']['choices']['message']['content']['text']
        index = datas.find('[')
        index2 = datas.find(']')
        substring = datas[index:index2 + 1]
        result = json.loads(substring)
    print(time.time()-t1)
    return result



if __name__ == "__main__":
    res = llm_chat_tran()
    print(res)
    #[{'user_id': 28, 'group_id': 3, 'group_name': '硬件/半导体组'}, {'user_id': 29, 'group_id': 4, 'group_name': '制造业组'}]
    #[{'user_id': 28, 'group_id': 3, 'group_name': '硬件/半导体组'}, {'user_id': 29, 'group_id': 4, 'group_name': '制造业组'}]

    res2 = llm_chat_zhizengzeng()
    print(res2)







