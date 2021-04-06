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
    INVALID_PARAMS = (20010, '无效参数')
    PARAMS_CHECK_FAILD = (20011, '参数检查失败')

    # 30001～40000 预留业务状态
    NO_DATA = (30001, '未查询到数据')

    REMOVE_NODE_SUCC = (30100, '删除节点成功')
    REMOVE_NODE_FAILD = (30101, '删除节点失败')
    REGISTER_SERVICE_SUCC = (30102, '注册节点成功')
    REGISTER_SERVICE_FAILD = (30103, '注册节点失败')
    NONE_SERVICES = (30104, '未发现任何节点')
