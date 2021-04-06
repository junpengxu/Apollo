# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:19 上午
# @Author  : xu.junpeng

# server info
SERVER_PORT = 8000
REGISTER_SERVER_NAME = "weakee_server"


DB_URI = 'mysql+pymysql://root:123456@localhost:13306/weakee'
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# celery config
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_RESULT_SERIALIZER = 'msgpack'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间
CELERY_ACCEPT_CONTENT = ["msgpack"]  # 指定任务接受的内容序列化的类型.
