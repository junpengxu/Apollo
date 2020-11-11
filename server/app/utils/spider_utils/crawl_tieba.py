# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 12:43 下午
# @Author  : xu.junpeng

import time
import json
import datetime
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from app.controllers.tieba import TiebaController

driver = webdriver.Chrome()


class Crawl:
    def __init__(self, topic_id, start_page, end_page, crawl_interval=0.02):
        self.topic_id = topic_id
        self.crawl_interval = crawl_interval
        self.request_url = "https://tieba.baidu.com/p/{}?pn={}"  # 默认从第一页开始爬
        self.request_reply_url = "https://tieba.baidu.com/p/totalComment?t={}&tid={}&fid=5577283&pn={}&see_lz=0"  # time, topic_id,
        self.request = requests
        self.request_head = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        self.start_page = start_page
        self.end_page = end_page
        self.driver = webdriver.Chrome()
        self.driver.get(self.request_url.format(self.topic_id, 1))
        self.request_cookies = None
        self.__gene_request_cookies()
        self.driver.close()

    def __gene_request_cookies(self):
        cookies = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
        cookies = '; '.join(item for item in cookies)
        self.request_head.update({"Cookie": cookies})

    def process_webpage(self, page):
        soup_html = BeautifulSoup(self.request.get(
            url=self.request_url.format(self.topic_id, page), headers=self.request_head).content,
                                  features="html.parser")

        page_content = soup_html.find_all('div', attrs={'class': 'l_post l_post_bright j_l_post clearfix'})
        reply_data = self.request.get(
            self.request_reply_url.format(int(time.time() * 1000), self.topic_id, page)).json()
        if reply_data["errno"] != 0:
            print("get reply data raise error")
            comment_info = {}
        else:
            comment_info = reply_data["data"]["comment_list"]

        for floor in page_content:
            # get user info
            floor_user_info = json.loads(floor.attrs["data-field"])["author"]
            floor_user_id = floor_user_info["user_id"]  # 本层发帖用户id
            user_name = floor_user_info["user_name"]
            user_nickname = floor_user_info["user_nickname"]
            avatar_attrs = floor.find('a', attrs={'class': 'p_author_face'}).find('img').attrs
            if "data-tb-lazyload" in avatar_attrs:
                avatar = avatar_attrs["data-tb-lazyload"]
            else:
                avatar = avatar_attrs["src"]

            print(floor_user_id, user_name, user_nickname, avatar)
            TiebaController().create_user(user_id=floor_user_id, user_name=user_name, avatar=avatar,
                                          user_nickname=user_nickname)

            # get topic info
            floor_content = floor.find('div', attrs={'class': 'd_post_content j_d_post_content'}).text
            post_id = floor.attrs["data-pid"]
            floor_tail_info = floor.find('div', attrs={'class': "post-tail-wrap"}).find_all('span', attrs={
                'class': 'tail-info'})

            public_device = ''
            floor_id = floor_tail_info[-2].text
            publish_time = floor_tail_info[-1].text
            if len(floor_tail_info) == 3:
                public_device = floor_tail_info[0].text

            TiebaController().create_post(
                topic_id=self.topic_id, content=floor_content, user_id=floor_user_id, publish_time=publish_time,
                floor_id=floor_id, public_device=public_device, post_id=post_id)
            # get reply info

            replys = comment_info.get(post_id)
            if not replys: continue
            for reply in replys["comment_info"]:
                TiebaController().create_reply(
                    content=reply["content"],
                    post_id=reply["post_id"],
                    user_id=reply["user_id"],
                    reply_id=reply["comment_id"],
                    reply_time=datetime.datetime.fromtimestamp(reply["now_time"]),
                    floor_id=floor_id,
                )
        # get reply

    def save(self):
        """
        按层保存，保存层主信息， 楼层内容， 回复内容
        :return:
        """
        pass

    def run(self):
        for page in range(self.start_page, self.end_page):
            time.sleep(self.crawl_interval)  # 避免爬的速度过快产生其他问题
            self.process_webpage(page)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
