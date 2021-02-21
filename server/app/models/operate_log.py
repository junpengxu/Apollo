# -*- coding: utf-8 -*-
# @Time    : 2020/12/13 2:00 上午
# @Author  : xu.junpeng

from app.base.basemodel import BaseModel, db


class OperateLog(db.Model, BaseModel):
    __tablename__ = 'operate_log'
    id = db.Column(db.Integer, primary_key=True)
    executor = db.Column(db.String(64), comment="操作人")
    action = db.Column(db.String(128), comment="接口行为描述")
    params = db.Column(db.Text, comment="携带的参数")
    router = db.Column(db.String(128), comment="请求的路由名称")
    remote_ip = db.Column(db.String(32), comment="远端请求ip")
