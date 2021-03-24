# -*- coding: utf-8 -*-
# @Time    : 2021/3/23 12:36 上午
# @Author  : xu.junpeng
import json
from app.models import OperateLog
from sqlalchemy import and_, or_


class OperateLogController:

    @classmethod
    def add_log(cls, executor, action, router, remote_ip, params):
        try:
            op = OperateLog(executor=executor, action=action, router=router, remote_ip=remote_ip, params=params)
            op.save()
            return True
        except:
            return False

    @classmethod
    def query_log(cls, page=1, offset=1000, content=None, **query):
        result = []
        _q = and_()
        if content:
            _q = and_(_q, OperateLog.action.like("%" + content + "%"))
        logs = OperateLog.query.filter(_q).order_by(OperateLog.id.desc()).paginate(
            page=page, per_page=offset, error_out=False).items
        total_nums = OperateLog.query.filter(_q).count()
        for log_info in logs:
            result.append({
                "executor": log_info.executor,
                "action": log_info.action,
                "remote_ip": log_info.remote_ip,
                "router": log_info.router,
                "create_time": log_info.create_time.strftime("%Y年%m月%d日 %H时%M分%S秒"),
                "params": log_info.params,
            })
        res = {"result": result, "total_nums": total_nums}
        return res
