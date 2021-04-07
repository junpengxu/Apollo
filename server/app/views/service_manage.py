# -*- coding: utf-8 -*-
# @Time    : 2021/4/2 上午12:51
# @Author  : xu.junpeng
from app.base.baseview import BaseView
from ..controllers import UserController
from app.base.status_code import Codes

from app.utils.service_manager import ServiceManager
from app import redis_cli
from app import app_config
import json
from datetime import datetime


class RegisterServiceNode(BaseView):
    def post(self):
        params = self.request.form
        node_name = params.get("node_name", None)
        node_host = params.get("node_host", None)
        node_port = params.get("node_port", None)
        node_register_time = params.get("node_register_time", None)
        if not (node_name and node_port and node_host and node_register_time):
            return self.formattingData(code=Codes.PARAMS_CHECK_FAILD.code, msg=Codes.PARAMS_CHECK_FAILD.desc, data=None)
        node_info = {
            "node_name": node_name,
            "node_host": node_host,
            "node_port": node_port,
            "node_register_time": node_register_time
        }
        if ServiceManager().service_register(node_info):
            return self.formattingData(
                code=Codes.REGISTER_SERVICE_SUCC.code, msg=Codes.REGISTER_SERVICE_SUCC.desc, data=None
            )
        return self.formattingData(
            code=Codes.REGISTER_SERVICE_FAILD.code, msg=Codes.REGISTER_SERVICE_FAILD.desc, data=None
        )


class GetAllService(BaseView):
    def post(self):
        params = self.request.json
        page = params.get("page", 0)
        offset = params.get("offset", 20)
        result = ServiceManager().get_all_service()
        services = result[(page - 1) * offset: page * offset]
        for node in services:
            node["node_register_time"] = datetime.fromtimestamp(float(node["node_register_time"])).strftime(
                "%Y年%m月%d日 %H时%M分%S秒")

        data = {"data": services, "total_nums": len(result)}
        if result:
            return self.formattingData(code=Codes.SUCCESS.code, msg=Codes.SUCCESS.desc, data=data)
        else:
            return self.formattingData(code=Codes.NONE_SERVICES.code, msg=Codes.NONE_SERVICES.desc, data=None)


class GetService(BaseView):
    def post(self):
        result = ServiceManager().get_all_service()
        data = {"data": result, "total_nums": len(result)}
        if result:
            return self.formattingData(code=Codes.SUCCESS.code, msg=Codes.SUCCESS.desc, data=data)
        else:
            return self.formattingData(code=Codes.NONE_SERVICES.code, msg=Codes.NONE_SERVICES.desc, data=None)


class DestroyService(BaseView):
    def post(self):
        params = self.request.form
        node_name = params.get("node_name", None)
        if not node_name:
            return self.formattingData(code=Codes.INVALID_PARAMS.code, msg=Codes.INVALID_PARAMS.desc, data=None)
        if ServiceManager().service_destroy(node_name):
            return self.formattingData(code=Codes.REMOVE_NODE_SUCC.code, msg=Codes.REMOVE_NODE_SUCC.desc, data=None)
        else:
            return self.formattingData(code=Codes.REMOVE_NODE_FAILD.code, msg=Codes.REMOVE_NODE_FAILD.desc, data=None)
