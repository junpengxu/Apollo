# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng
# @File    : view

from app.base.baseview import BaseView
from app.base.status_code import Codes
from app.task import add


class Ping(BaseView):
    def get(self):
        add.delay()
        return self.formattingData(code=Codes.SUCCESS.code, msg="ping", data=None)
