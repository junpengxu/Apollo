# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 9:34 上午
# @Author  : xu.junpeng

from app.views import Ping, CreateAccount, Login, UserInfo, Logout
from app.views import CreateSpiderTask, SearchSpiderTask, GetTopicDetail
from app.views.operate_log import OperateLog
from app.views.service_manage import RegisterServiceNode, GetAllService, DestroyService

def bind_urls(app):
    ##########
    # user
    ##########
    app.add_url_rule('/ping', view_func=Ping.as_view('ping'), methods=['GET'])
    app.add_url_rule(
        '/user/create', view_func=CreateAccount.as_view('create_account'), methods=['POST'])
    app.add_url_rule(
        '/user/login', view_func=Login.as_view('login'), methods=['POST'])
    app.add_url_rule(
        '/user/logout', view_func=Logout.as_view('logout'), methods=['POST'])
    app.add_url_rule(
        '/user/info', view_func=UserInfo.as_view('get_user_info'), methods=['GET'])
    app.add_url_rule(
        '/user/logout', view_func=UserInfo.as_view('log_out'), methods=['POST'])

    ##########
    # spider
    ##########
    app.add_url_rule(
        '/spider/create_task', view_func=CreateSpiderTask.as_view('create_spider_task'), methods=['POST']
    )
    app.add_url_rule(
        '/spider/search_task', view_func=SearchSpiderTask.as_view('search_spider_task'), methods=['POST']
    )
    app.add_url_rule(
        '/spider/search_tieba_task_result',
        view_func=GetTopicDetail.as_view('search_tieba_task_result'),
        methods=['POST']
    )

    ##########
    # operate log
    ##########

    app.add_url_rule(
        '/operate_log/search', view_func=OperateLog.as_view('operate_log_search'), methods=['POST']
    )

    ##########
    # service register manager
    ##########

    app.add_url_rule(
        '/service_manage/register_service', view_func=RegisterServiceNode.as_view('register_service'), methods=['POST']
    )
    app.add_url_rule(
        '/service_manage/get_all_service', view_func=GetAllService.as_view('get_all_service'), methods=['POST']
    )
    app.add_url_rule(
        '/service_manage/register_service', view_func=DestroyService.as_view('destroy_service'), methods=['POST']
    )
