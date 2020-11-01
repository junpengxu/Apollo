# -*- coding: utf-8 -*-
# @Time    : 2020/10/25 5:20 下午
# @Author  : xu.junpeng

from app.models import Ping


class PingController:

    @classmethod
    def create_task(cls):
        try:
            ping = Ping()
            ping.save()
            return True
        except:
            return False
