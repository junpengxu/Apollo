# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng
# @File    : view

from app.base.baseview import BaseView
from ..controllers import UserController
from app.base.status_code import Codes
from app.utils.token import generate_token
from app import redis_cli
from app import app_config
import json


class CreateAccount(BaseView):
    def post(self):
        params = self.request.form
        username = params.get("username", None)
        password = params.get("password", None)

        if UserController.create_user(username=username, password=password):
            return self.formattingData(code=Codes.SUCCESS.code, msg='用户创建成功', data=None)
        return self.formattingData(code=Codes.FAILE.code, msg='用户创建失败', data=None)


class Login(BaseView):
    def post(self):
        params = self.request.json
        username = params.get("username", None)
        password = params.get("password", None)
        if username and password and UserController.login(username=username, password=password):
            token = generate_token(key=username)
            user_info = {"username": username}
            redis_cli["token"].set(name=token, value=json.dumps(user_info), ex=app_config.USER_TOKEN_EXPIRE_TIME)
            return self.formattingData(code=Codes.SUCCESS.code, msg='用户登陆成功', data={"token": token})
        return self.formattingData(code=Codes.FAILE.code, msg='用户登陆失败', data=None)


class Logout(BaseView):
    def post(self):
        return self.formattingData(code=Codes.SUCCESS.code, msg='退出登陆', data=None)


class UserInfo(BaseView):
    def get(self):
        return self.formattingData(code=Codes.SUCCESS.code, msg='获取用户信息', data={
            "roles": ['admins'],
            "introduction": "this is introduction",
            "name": "weakee",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
        })
