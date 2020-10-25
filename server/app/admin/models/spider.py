# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 5:21 下午
# @Author  : xu.junpeng


from app.base.basemodel import BaseModel, db


class Tieba(db.Model, BaseModel):
    __tablename__ = 'tieba_spider'
    id = db.Column(db.Integer, primary_key=True)
    request_url = db.Column(db.String(64), unique=True)
    request_headers = db.Column(db.Text)
    start_page = db.Column(db.Integer)
    end_page = db.Column(db.Integer)
