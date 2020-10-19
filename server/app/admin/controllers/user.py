# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng

from ..models import User


class UserController:

    @classmethod
    def create_user(cls, username, password):
        try:
            user = User(username=username, password=password)
            user.save()
            return True
        except:
            return False

    @classmethod
    def login(cls, username, password):
        user = User.query.filter((User.username == username)).first()
        if not user:
            return False
        if user.verify_password(password):
            return True
        return False
