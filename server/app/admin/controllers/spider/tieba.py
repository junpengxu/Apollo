# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 5:20 下午
# @Author  : xu.junpeng

from ...models import Tieba


class TiebaController:

    @classmethod
    def create_task(cls, url, headers, start_page, end_page):
        try:
            task = Tieba(
                request_url=url,
                request_headers=headers,
                start_page=start_page,
                end_page=end_page
            )
            task.save()
            return True
        except:
            return False
