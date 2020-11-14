# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 5:21 下午
# @Author  : xu.junpeng


from app.base.basemodel import BaseModel, db


class Spider(db.Model, BaseModel):
    __tablename__ = 'spider'
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(2048))
    topic_id = db.Column(db.BigInteger)
