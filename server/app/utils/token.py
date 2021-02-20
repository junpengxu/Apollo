# -*- coding: utf-8 -*-
# @Time    : 2021/2/20 11:24 下午
# @Author  : xu.junpeng

import time
import base64
import hmac
from app import app_config

def generate_token(key, expire=app_config.USER_TOKEN_EXPIRE_TIME):
    """
    @Args:
        key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
        expire: int(最大有效时间，单位为s)
    @Return:
        state: str
    :param key:
    :param expire:
    :return:
    """
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshex_str = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshex_str
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))

    return b64_token.decode("utf-8")


def certify_token(key, token):
    """
    @Args:
        key: str
        token: str
    @Returns:
        boolean
    :param key:
    :param token:
    :return:
    """
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True
