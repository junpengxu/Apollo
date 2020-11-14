# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng
# @File    : view

from app.base.baseview import BaseView
from app.base.status_code import Codes

from app.controllers import SpiderController
from app.task.spider_tasks import run_zongyue_tieba_spider
from app.controllers.tieba import TiebaController


class CreateSpiderTask(BaseView):
    def post(self):
        params = self.request.json
        topic_id = params.get("topic_id")
        desc = params.get("desc")
        run_zongyue_tieba_spider.delay(topic_id=topic_id)
        if SpiderController.create_task(topic_id, desc):
            return self.formattingData(code=Codes.SUCCESS.code, msg='任务创建成功', data=None)
        return self.formattingData(code=Codes.FAILE.code, msg='任务创建失败', data=None)


class SearchSpiderTask(BaseView):
    def post(self):
        params = self.request.json
        page = int(params.get("page", 1))
        offset = int(params.get("offset", 20))
        content = params.get("content")
        query = params.get("query", {})
        result, total_nums = SpiderController.search_task(page, offset, content, **query).values()
        if len(result) == 0:
            return self.formattingData(code=Codes.FAILE.code, msg='未查询到数据', data=None)
        return self.formattingData(code=Codes.SUCCESS.code, msg='搜索完成', data={"data": result, "total_nums": total_nums})


class searchTaskSesult(BaseView):
    def post(self):
        params = self.request.json
        page = int(params.get("page", 1))
        offset = int(params.get("offset", 20))
        content = params.get("content")
        query = params.get("query", {})
        result, total_nums = SpiderController.search_task(page, offset, content, **query).values()
        if len(result) == 0:
            return self.formattingData(code=Codes.FAILE.code, msg='未查询到数据', data=None)
        for index, item in enumerate(result):
            result[index]["url"] = item["request_url"]
            del result[index]["request_url"]
        return self.formattingData(code=Codes.SUCCESS.code, msg='搜索完成', data={"data": result, "total_nums": total_nums})


class getTopicDetail(BaseView):
    def post(self):
        params = self.request.json
        page = int(params.get("page", 1))
        offset = int(params.get("offset", 20))
        topic_id = params.get("topic_id")
        # 直接组装好数据
        posts = TiebaController.get_posts_by_topic_id(topic_id, page, offset)
        post_ids = [post["post_id"] for post in posts]
        replys = TiebaController.get_reply_by_posts(post_ids)
        user_ids = [reply["user_id"] for reply in replys.values()]
        users = TiebaController.get_user_info_by_user_ids(user_ids)
        return self.formattingData(code=Codes.SUCCESS.code, msg='搜索完成', data={
            "post_info": posts,
            "user_info": users,
            "reply_info": replys,
            "total_nums": len(posts)
        })
