# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 12:57 上午
# @Author  : xu.junpeng

from enum import unique
from app.base.baseenum import EnumBase


@unique
class Codes(EnumBase):
    # 20000～30000 预留系统状态
    SUCCESS = (20000, '操作成功')
    FAILE = (20001, '操作失败')
    LOGOUT = (20002, '退出登陆成功')
    TOKEN_INVALID = (20003, 'token失效')

    # 30001～40000 预留业务状态
    NO_DATA = (30001, '未查询到数据')
