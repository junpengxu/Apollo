# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 9:31 上午
# @Author  : xu.junpeng
from flask import request, jsonify
from flask.views import MethodView


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
        return super(BaseView, self).dispatch_request(*args, **kwargs)
