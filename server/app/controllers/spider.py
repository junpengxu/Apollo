# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 5:20 下午
# @Author  : xu.junpeng

from app.models import Spider, BaiduTiebaTopic
from sqlalchemy import and_


class SpiderController:

    @classmethod
    def create_task(cls, topic_id, desc):
        try:
            task = Spider(
                topic_id=topic_id,
                desc=desc,
            )
            task.save()
            return True
        except:
            return False

    @classmethod
    def search_task(cls, page=1, offset=1000, content=None, **query):
        """
        :param page: 起始页面
        :param offset: 每页查询数量
        :param content: 查找条件， 用来固定一个查询的字段与业务做绑定，
                e.g _q = Model.name.like('%' + content + '%')
        :param query: 匹配条件
        :return:
        """
        result = []
        _q = and_()
        tasks = Spider.query.filter(_q).order_by(Spider.id.desc()).paginate(
            page=page, per_page=offset, error_out=False).items
        topic_ids = [task.topic_id for task in tasks]
        total_nums = Spider.query.filter(_q).count()
        topics = BaiduTiebaTopic.query.filter(BaiduTiebaTopic.topic_id.in_(topic_ids)).all()
        topics = {topic.topic_id: topic for topic in topics}
        for task in tasks:
            try:
                topic = topics[task.topic_id]
                result.append({
                    "id": task.id,
                    "desc": task.desc,
                    "create_time": task.create_time,
                    "update_time": task.update_time,
                    "topic_id": topic.topic_id,
                    "topic_url": topic.url,
                    "topic_title": topic.title,
                    'crawl_page': topic.crawl_page
                })
            except Exception as e:
                print(e)

        return {"result": result, "total_nums": total_nums}

    @classmethod
    def get_task(cls, pk):
        pass
