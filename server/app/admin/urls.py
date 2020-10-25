# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 9:34 上午
# @Author  : xu.junpeng

from app.admin.views import Ping, CreateAccount, Login, userInfo, Logout
from app.admin.views import ZongYue as ZongYueSpider


def bind_urls(app):
    app.add_url_rule('/ping', view_func=Ping.as_view('ping'), methods=['GET'])
    app.add_url_rule(
        '/user/create', view_func=CreateAccount.as_view('create_account'), methods=['POST'])
    app.add_url_rule(
        '/user/login', view_func=Login.as_view('login'), methods=['POST'])
    app.add_url_rule(
        '/user/logout', view_func=Logout.as_view('logout'), methods=['POST'])
    app.add_url_rule(
        '/user/info', view_func=userInfo.as_view('get_user_info'), methods=['GET'])
    app.add_url_rule(
        '/user/logout', view_func=userInfo.as_view('log_out'), methods=['POST'])

    ##########
    # spider
    ##########
    app.add_url_rule(
        '/spider/zongyue', view_func=ZongYueSpider.as_view('zongyue_tieba_spider'), methods=['POST'])
