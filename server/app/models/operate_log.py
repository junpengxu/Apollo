# -*- coding: utf-8 -*-
# @Time    : 2020/12/13 2:00 上午
# @Author  : xu.junpeng

from app.base.basemodel import BaseModel, db


class OperateLog(db.Model, BaseModel):
    __tablename__ = 'operate_log'
    id = db.Column(db.Integer, primary_key=True)
    executor = db.Column(db.Integer, comment="操作人")
    action = db.Column(db.BigInteger, comment="接口行为描述")
    params = db.Column(db.Text, comment="携带的参数")
    router = db.Column(db.String(128), comment="请求的路由名称")
    # status = 1 # 操作是否成功
