# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:12 上午
# @Author  : xu.junpeng
# @File    : view
from app.base.baseview import BaseView
from app.base.status_code import Codes

from app.controllers import SpiderController
from app.tasks.spider_tasks import run_zongyue_tieba_spider
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
        for item in result:
            item["update_time"] = item["update_time"].strftime("%Y年%m月%d日 %H时%M分%S秒")
        if len(result) == 0:
            return self.formattingData(code=Codes.FAILE.code, msg='未查询到数据', data=None)
        return self.formattingData(code=Codes.SUCCESS.code, msg='搜索完成', data={"data": result, "total_nums": total_nums})


class GetTopicDetail(BaseView):
    def post(self):
        params = self.request.json
        page = int(params.get("page", 1))
        offset = int(params.get("offset", 20))
        topic_id = params.get("topic_id")
        content = params.get("content")
        # 直接组装好数据
        posts, total_nums = TiebaController.search_post_from_topic(
            topic_id=topic_id, content=content, page=page, offset=offset
        ).values()
        topic_info = TiebaController.get_topic_info_by_topic_id(topic_id)
        post_ids = [post["post_id"] for post in posts]

        replys = TiebaController.get_reply_by_posts(post_ids)

        # format reply data structure
        reply_data = {}
        for reply in replys:
            if reply["post_id"] not in reply_data:
                reply_data[reply["post_id"]] = []
            reply_data[reply["post_id"]].append(
                {
                    "content": reply["content"],
                    "user_id": reply["user_id"],
                    "reply_time": reply["reply_time"].strftime("%Y年%m月%d日 %H时%M分%S秒"),
                }
            )
        user_ids = [post["user_id"] for post in posts]
        users = TiebaController.get_user_info_by_user_ids(user_ids)
        for item in posts:
            item["nickname"] = users[item["user_id"]]["nickname"] or users[item["user_id"]]["user_name"]
            item["avatar"] = users[item["user_id"]]["avatar"]
            item["publish_time"] = item["publish_time"].strftime("%Y年%m月%d日 %H时%M分%S秒")
            item["topic_url"] = topic_info["topic_url"] + str(item["page"])
        return self.formattingData(code=Codes.SUCCESS.code, msg='搜索完成', data={
            "post_info": posts,
            "user_info": users,
            "reply_info": reply_data,
            "total_nums": total_nums
        })
