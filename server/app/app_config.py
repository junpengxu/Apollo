# -*- coding: utf-8 -*-
# @Time    : 2021/2/21 12:38 上午
# @Author  : xu.junpeng

# redis config
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
REDIS_TOEKN_DB = 15

USER_TOKEN_EXPIRE_TIME = 24 * 60 * 60

# WHITE_LIST

WHITE_LIST = [
    '/user/login',
    '/user/info',
]
