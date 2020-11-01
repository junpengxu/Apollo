# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:31 上午
# @Author  : xu.junpeng

from app.base.basemodel import BaseModel, db


class Ping(db.Model, BaseModel):
    __tablename__ = 'ping'
    id = db.Column(db.Integer, primary_key=True)
