# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 9:31 上午
# @Author  : xu.junpeng
from flask import request, jsonify
from flask.views import MethodView
from app import redis_cli
# from app.utils.token import certify_token # TODO 完善token 校验机制
from app.base.status_code import Codes
import json
from app import app_config
from app.utils.operate_info import record_opterate_log


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.__setattr__('request', request)
        super(BaseView, self).__init__(*args, **kwargs)

    def formattingData(self, code, msg, data):
        return jsonify(
            {
                "code": code,
                "msg": msg,
                "data": data
            }
        )

    def dispatch_request(self, *args, **kwargs):
        executor = "unknown"
        if self.request.url_rule.rule not in app_config.WHITE_LIST:
            token = self.request.cookies.get("Token")
            if token:
                user_info = json.loads(redis_cli["token"].get(name=token))
                if user_info:
                    executor = user_info["username"]
                else:
                    return self.formattingData(code=Codes.TOKEN_INVALID.code, msg=Codes.TOKEN_INVALID.desc, data=None)
            else:
                return self.formattingData(code=Codes.TOKEN_INVALID.code, msg=Codes.TOKEN_INVALID.desc, data=None)
        record_opterate_log.delay(
            executor=executor,
            remote_ip=self.request.remote_addr,
            params=json.dumps(self.request.json),
            router=self.request.url_rule.rule,
            action=self.request.url_rule.endpoint
        )
        return super(BaseView, self).dispatch_request(*args, **kwargs)
