# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 5:20 下午
# @Author  : xu.junpeng

from ...models import Spider
from sqlalchemy import and_


class SpiderController:

    @classmethod
    def create_task(cls, url, desc, headers, start_page, end_page):
        try:
            task = Spider(
                request_url=url,
                desc=desc,
                request_headers=headers,
                start_page=start_page,
                end_page=end_page
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
        total_nums = Spider.query.filter(_q).order_by(Spider.id.desc()).count()
        for task in tasks:
            result.append({
                "id": task.id,
                "desc": task.desc,
                "request_url": task.request_url,
                "request_headers": task.request_headers,
                "start_page": task.start_page,
                "end_page": task.start_page
            })
        return {"result": result, "total_nums": total_nums}

    @classmethod
    def get_task(cls, pk):
        pass
