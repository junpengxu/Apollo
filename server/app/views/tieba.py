# -*- coding: utf-8 -*-
# @Time    : 2021/1/30 1:12 上午
# @Author  : xu.junpeng
import json
from app.base.baseview import BaseView
from ..controllers import TiebaController
from app.base.status_code import Codes


class SearchPostFromTopic(BaseView):
    def post(self):
        params = self.request.json
        content = params.get("content")
        query = json.loads(params.get("offset", '{}'))
        topic_id = params.get("topic_id")
        result = TiebaController.search_post_from_topic(content=content, topic_id=topic_id, query=query)
        return self.formattingData(code=Codes.SUCCESS.code, msg='搜索完成',
                                   data={"data": result, "total_nums": len(result)})
