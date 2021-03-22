# -*- coding: utf-8 -*-
# @Time    : 2021/2/21 11:11 上午
# @Author  : xu.junpeng

from app.controllers import OperateLogController
from app import celery

@celery.task
def record_opterate_log(executor, action, router, remote_ip, params):
    # 只记录登陆用户的操作
    OperateLogController.add_log(executor=executor, action=action, router=router, remote_ip=remote_ip, params=params)
