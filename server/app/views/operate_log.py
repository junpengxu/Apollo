# -*- coding: utf-8 -*-
# @Time    : 2021/3/23 12:33 上午
# @Author  : xu.junpeng

from app.base.baseview import BaseView
from app.base.status_code import Codes
from app.controllers.operate_log import OperateLogController


class OperateLog(BaseView):
    def post(self):
        params = self.request.json
        page = params.get("page", 0)
        offset = params.get("offset", 20)
        content = params.get("content", None)
        # query = params.get("filter", {})
        result, total_num = OperateLogController.query_log(page=page, offset=offset, content=content).values()
        if not total_num:
            return self.formattingData(code=Codes.NO_DATA.code, msg=Codes.NO_DATA.desc, data=[])
        data = {"data": result, "total_nums": total_num}
        return self.formattingData(code=Codes.SUCCESS.code, msg=Codes.SUCCESS.desc, data=data)

