# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng
# @File    : view

from app.base.baseview import BaseView
from ..controllers import UserController
from app.base.status_code import Codes


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

        if UserController.login(username=username, password=password):
            return self.formattingData(code=Codes.SUCCESS.code, msg='用户登陆成功', data=None)
        return self.formattingData(code=Codes.FAILE.code, msg='用户登陆失败', data=None)
