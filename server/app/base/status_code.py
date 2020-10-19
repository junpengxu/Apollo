# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 12:57 上午
# @Author  : xu.junpeng

from enum import unique
from app.base.baseenum import EnumBase


@unique
class Codes(EnumBase):
    SUCCESS = (20000, '操作成功')
    FAILE = (20001, '操作失败')
    LOGOUT = (20002, '退出登陆成功')
