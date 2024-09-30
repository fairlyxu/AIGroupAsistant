import traceback
from flask import jsonify, abort, request, Blueprint
from dbtool.sql_helper import sqlhelper
from utils.llm_helper import llm_chat_tran

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
    print("data:",data)
    requestid = data.get('requestid')
    num = data.get('num')
    activity_id = data.get('activaty_id')
    regroup_users_ids = data.get('users')
    if not requestid or not num or not activity_id or not regroup_users_ids:
        abort(400)
    try:
        all_users = sqlhelper.get_task_by_requestid(activity_id)
        remain_users = []
        regroup_users = []

        for user in all_users:
            if user[0] not in regroup_users:
                remain_users.append(user)
            else:
                regroup_users.append((user[0], user[1], user[2], user[3]))

        # 调用llm模型，生成分组信息
        llm_res = llm_chat_tran(remain_users, regroup_users, num)
        print("llm_res:", llm_res)

        #llm_res = [{'user_id': 28, 'group_id': 3, 'group_name': '硬件/半导体组'},  {'user_id': 29, 'group_id': 4, 'group_name': '制造业组'}]

        # 更新分组信息，插入数据库
        unique_groups = []
        seen_group_ids = set({t[4] for t in all_users})
        for record in llm_res:
            user_id = record['user_id']
            group_id = record['group_id']
            group_name = record['group_name']
            output.append({'id':user_id,'group':group_id})
            if group_id not in seen_group_ids:
                unique_groups.append({'activity_id':activity_id,'group_id': group_id, 'group_name': group_name})
                seen_group_ids.add(group_id)
        sqlhelper.create_groups(unique_groups)
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

