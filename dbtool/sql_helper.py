# -*-coding:utf-8 -*-
"""
# File       : llm_helper.py.py
# Time       ：2024/9/29 11:46
# Author     ：fairyxu
# Description：
"""
import pymysql
from dbutils.pooled_db import PooledDB
from conf.server_config import SERVER_CONFIG
import traceback
class SqlHelper:
    def __init__(self) -> None:
        self.pool = PooledDB(
            creator=pymysql,  # 使用pymysql作为连接的创建者
            maxconnections=20,  # 连接池中最大连接数
            mincached=2,  # 连接池中最小空闲连接数
            maxcached=20,  # 连接池中最大空闲连接数
            maxshared=20,  # 连接池中最大共享连接数
            blocking=True,  # 如果连接池达到最大连接数，是否等待连接释放后再获取新连接
            host=SERVER_CONFIG['DBConfig'].HOSTNAME,  # 数据库主机名
            port=SERVER_CONFIG['DBConfig'].PORT,  # 数据库端口号
            user=SERVER_CONFIG['DBConfig'].USERNAME,  # 数据库用户名
            password=SERVER_CONFIG['DBConfig'].PASSWORD,  # 数据库密码
            database=SERVER_CONFIG['DBConfig'].DATABASE,  # 数据库名称
            charset='utf8mb4'  # 数据库字符集
        )

        #self.dbname = ''#SERVER_CONFIG['DBConfig'].DATABASE

    def create_groups(self, groups):
        data = [
            {'activity_id':1,'group_id': 3, 'group_name': '硬件/半导体组'},
            {'activity_id':1,'group_id': 4, 'group_name': '制造业组'}
        ]
        with self as db:
            try:
                table_name = 'yuanyu_activity_group'
                columns = ['group_id', 'group_name','activity_id']
                # 构建插入语句
                values_str = ', '.join( [f"({activity_id},{group_id}, '{group_name}')" for activity_id, group_id, group_name in groups])
                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {values_str};"
                print(insert_query)
                db.cursor.execute(insert_query)
                db.conn.commit()
                print("create_groups success！！！！")
            except Exception as e:
                db.conn.rollback()
                traceback.print_exc()
                print("create_groups error！！！！")

    def get_users_by_ids(self, ids = [], activeid=1):
        with self as db:
            try:
                query = "SELECT * FROM yuanyu_activity_user WHERE id IN (%s) AND activity_id = %d" % (','.join(['%s'] * len(ids)), '%d')
                parameters = ids + (activeid,)
                db.cursor.execute(query, parameters)
                return db.cursor.fetchall()
            except Exception as e:
                traceback.print_exc()
                print("get_task_by_status error~:", e)

    def get_users_by_activity(self,activeid =1):
        with self as db:
            try:
                query = "SELECT id,industry,topic, self_introduction,result_group FROM yuanyu_activity_user WHERE  activity_id = %d" % (activeid)
                db.cursor.execute(query)
                return db.cursor.fetchall()
            except Exception as e:
                traceback.print_exc()
                print("get_task_by_status error~:", e)
    def update_users_group_info(self,user_datas):
        with self as db:
            try:
                # 表名
                table_name = 'yuanyu_activity_user'
                # 构建更新语句
                update_queries = []
                for item in user_datas:
                    query = f"UPDATE {table_name} SET group_id = {item['group_id']}  WHERE user_id = {item['user_id']};"
                    update_queries.append(query)
                db.cursor.execute(update_queries)
                print("update_users_group_info success！！！！")
            except Exception as e:
                traceback.print_exc()
                print("update_users_group_info success！！！！",e)

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()


sqlhelper = SqlHelper()
