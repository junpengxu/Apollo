# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 9:31 上午
# @Author  : xu.junpeng
from flask import request, jsonify
from flask.views import MethodView
from app import redis_cli
from app.utils.token import certify_token
from app.base.status_code import Codes
import json
from app import app_config


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.__setattr__('request', request)
        super(BaseView, self).__init__(*args, **kwargs)
        # 判断token是否可以继续进行, 如何在这里直接返回结果呢
        if self.request.environ['REQUEST_URI'] not in app_config.WHITE_LIST:
            token = self.request.cookies["Admin-Token"]
            # 只根据token做简单的校验
            user_info = redis_cli["token"].get(name=token)
            if user_info:
                user_info = json.loads(user_info)
                if certify_token(key=user_info["username"], token=token):
                    print("通过校验")
            else:
                return self.formattingData(code=Codes.TOKEN_INVALID.code, msg=Codes.TOKEN_INVALID.desc, data=None)

    def formattingData(self, code, msg, data):
        return jsonify(
            {
                "code": code,
                "msg": msg,
                "data": data
            }
        )

    def dispatch_request(self, *args, **kwargs):
        return super(BaseView, self).dispatch_request(*args, **kwargs)
