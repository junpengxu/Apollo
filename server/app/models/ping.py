# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:31 上午
# @Author  : xu.junpeng

from app.base.basemodel import BaseModel, db


class Video(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    leve1 = db.Column(db.String(255))
    leve2 = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    comments = db.relationship(
        'Comment', backref=db.backref('video'), lazy='dynamic')

    def __init__(self, id, title, url, leve1, leve2):
        self.id = id
        self.title = title
        self.url = url
        self.leve1 = leve1
        self.leve2 = leve2

    def __repr__(self):
        return '<FreeVideo %r>' % self.title

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "leve1": self.leve1,
            "leve2": self.leve2,
            "cover": self.cover
        }
