# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng
# @File    : view

from app.base.baseview import BaseView
from app.base.status_code import Codes

from app.admin.controllers import TiebaController


class ZongYue(BaseView):
    def post(self):
        params = self.request.json
        url = params.get("url")
        headers = params.get("headers")
        start_page = params.get("start_page")
        end_page = params.get("end_page")
        if TiebaController.create_task(url, headers, start_page, end_page):
            return self.formattingData(code=Codes.SUCCESS.code, msg='任务创建成功', data=None)
        return self.formattingData(code=Codes.FAILE.code, msg='任务创建失败', data=None)
