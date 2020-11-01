# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:31 上午
# @Author  : xu.junpeng


from app.base.basemodel import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    hashpwd = db.Column(db.String(128))

    @property
    def password(self):
        return self.hashpwd

    @password.setter
    def password(self, password):
        self.hashpwd = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashpwd, password)

    def __repr__(self):
        return f'<User {self.username}>'
