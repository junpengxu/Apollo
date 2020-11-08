# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng
# @File    : view

from app.task import add
from app.base.baseview import BaseView
from app.base.status_code import Codes
from app.utils.spider_utils.crawl_tieba import Crawl


class Ping(BaseView):
    def get(self):
        return self.formattingData(code=Codes.SUCCESS.code, msg="ping", data=None)
