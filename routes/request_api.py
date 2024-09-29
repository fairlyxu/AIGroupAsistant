import traceback
import json
from flask import jsonify, abort, request, Blueprint
#from dbtool.sql_helper import sqlhelper
import utils
import requests
REQUEST_API = Blueprint('request_api', __name__)
def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

@REQUEST_API.route('/generate', methods=['POST'])
def generate():
    print("enter gerequest")
    output = []
    code = 100
    msg = "排队中"

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    if not data.get('requestid'):
        print("requestid is not exist")
        abort(400)
    if not data.get('num'):
        print("num is not exist")
        abort(400)
    if not data.get('activaty_id'):
        print("activaty_id    is not exist")
        abort(400)
    if not data.get('users'):
        print("users    is not exist")
        abort(400)

    try:
        requestid = "8eaaaaadddssssdddd"
        num = 7
        activity_id=1
        users = [1, 2, 3, 4]
        #obj = sqlhelper.get_task_by_requestid(data.get('requestid'))



        #获取user id 的提交信息
        #obj = sqlhelper.get_users_by_ids(data.get('requestid'))
        results = [('1','云服务','亲子、AI、哲学','人工智能/培训/企业服务公司】丽台科技-英伟达GPU总代，冰特科技-自建算力平台，冰特算力学院-AI培训，英伟达深度学习中心-高中研学，元起点-灵活用工和知识产权','1','云服务组'),
                    ('3','硬件 / 半导体','AI在IT服务中的应用','网络安全行业技术人员','3','硬件/半导体组'),
                    ('4','制造业/趋势发展','无','大家电业务负责人','4','制造业组'),
                    ('5','医疗健康和生命科学','AI在营销中的应用','从医疗设备和耗材销售管理多年','5','医疗健康和生命科学组'),
                    ('6','医疗健康和生命科学','NIVIDA是否有在AI软件方面的布局考量，会在哪些领域做准备','连续创业者','5','医疗健康和生命科学组'),
                    ('7','云服务','AI可能的发展趋势','互联网从业者，现在做数字化转型相关工作','1','云服务组'),
                    ('8','硬件/半导体','中国AI大算力芯片设计公司的前途和出路','深耕半导体行业28年，负责苹果供应链16年，复旦大学EMBA，华东师范大学CTO学院产业导师','3','硬件/半导体组'),
                    ('9','医疗健康和生命科学','数字人医护','AI医疗科技公司，主要做医学服务','5','医疗健康和生命科学组'),
                    ('10','医疗健康和生命科学','无','22级1班陈伊君','5','医疗健康和生命科学组'),
                    ('11','建筑 / 工程 / 交通运输','想多了解元宇宙及AI计算目前的商用情况','企业服务公司，服务内容设计咨询、数字化转型及工业智能制造','6','建筑/工程/交通运输组'),
                    ('12','智慧城市/空间','英伟达芯片在智能分析领域的应用案例及未来规划','华启智能科技副总经理，分管技术中心','7','智慧城市/空间组'),
                    ('13','建筑/工程/交通运输','AI为工程咨询带来怎样的便捷和行业的改变','2022级1班17A，一家工程咨询公司的经营人','6','建筑/工程/交通运输组')]

        # 将结果转换为字符串
        result_strings = ['|'.join(map(str, row)) for row in results]

        # 将所有行拼接成一个字符串，使用换行符分隔
        final_string = '\n'.join(result_strings)





    except Exception as e:
        print("error:", e)
        traceback.print_exc()
        code = -1
        msg = "查询失败"

    res_data = {
        "code": code,
        "msg": msg,
        "data": output
    }

    # HTTP 201 Created
    return jsonify(res_data), 200

