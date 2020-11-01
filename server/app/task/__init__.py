# -*- coding: utf-8 -*-
# @Time    : 2020/11/1 11:49 上午
# @Author  : xu.junpeng
from app import celery
from app.controllers import PingController
from app.utils.logger import base_log
@celery.task
def add():
    PingController.create_task()
    base_log.logger.info("celery task run ")
