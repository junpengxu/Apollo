# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 12:43 下午
# @Author  : xu.junpeng
# 目前只能爬纵月六只鹅这个贴吧的数据，因为不同的贴吧，还没有找到通用的能提取数据的方法。大概是反爬措施吧
import time
import json
import datetime
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from app.controllers.tieba import TiebaController
from app.utils.logger import spider_log


# chrome_options = Options()

class Crawl:
    def __init__(self, topic_id, crawl_interval=0.02):
        self.topic_id = topic_id
        self.topic_title = None
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
        self.soup_html = None
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # self.driver = webdriver.Chrome(chrome_options = chrome_options)
        # self.driver.get(self.request_url.format(self.topic_id, 1))
        # self.request_cookies = None
        # self.__gene_request_cookies()
        # self.driver.close()
        self.now_page = 1
        self.topic_total_page_nums = 0

    def __gene_request_cookies(self):
        cookies = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
        cookies = '; '.join(item for item in cookies)
        self.request_head.update({"Cookie": cookies})

    def process_webpage(self):
        # 还没有找到通用的解析数据的方法， 使用or 拼接发现的格式
        # 1. 获取到当前页面
        soup_html = BeautifulSoup(self.request.get(
            url=self.request_url.format(self.topic_id, self.now_page)).content,
                                  features="html.parser")

        # 3. 提取出帖子相关的楼层信息，包括这个帖子在当前页面的发布信息，以及回复，以及用户的简要信息

        page_content = soup_html.find_all('div', attrs={'class': 'l_post l_post_bright j_l_post clearfix'})

        # 4. 通过回复接口拿到这个页面下所有的回复信息
        comment_info = self.extract_reply(now_page=self.now_page)
        # 没有数据的情况下，转换为空字典
        if comment_info == []:
            comment_info = {}

        # 5. 遍历当前页面下每一个post
        for floor in page_content:
            # 获取这一层的用户信息
            floor_user_info = self.extract_user_info(floor)
            floor_user_id = floor_user_info["user_id"]
            self.save_user(
                user_id=floor_user_id,
                user_name=floor_user_info["user_name"],
                avatar=floor_user_info["avatar"],
                nickname=floor_user_info["user_nickname"]
            )
            # 获取post(层)的信息
            post_info = self.extract_post(floor)
            self.save_post(
                topic_id=self.topic_id, content=post_info["content"],
                user_id=floor_user_id, publish_time=post_info["publish_time"],
                floor_id=post_info["floor_id"], public_device=post_info["public_device"],
                post_id=post_info["post_id"]
            )

            # get reply info
            replys = comment_info.get(post_info["post_id"])
            if not replys: continue
            for reply in replys["comment_info"]:
                self.save_reply(
                    content=reply["content"], post_id=reply["post_id"], user_id=reply["user_id"],
                    reply_id=reply["comment_id"],
                    reply_time=datetime.datetime.fromtimestamp(reply["now_time"]), floor_id=post_info["floor_id"]
                )

    def extract_user_info(self, floor):
        user_info = json.loads(floor.attrs["data-field"])["author"]
        user_id = user_info["user_id"]  # 本层发帖用户id
        user_name = user_info.get("user_name", "uncatch")
        user_nickname = user_info.get("user_nickname", "uncatch")
        avatar_attrs = floor.find('a', attrs={'class': 'p_author_face'}).find('img').attrs
        if "data-tb-lazyload" in avatar_attrs:
            avatar = avatar_attrs.get("data-tb-lazyload", "")
        else:
            avatar = avatar_attrs.get("src", "")
        user_info = {
            "user_id": user_id,
            "user_name": user_name,
            "avatar": avatar,
            "user_nickname": user_nickname,
        }
        return user_info

    def extract_post(self, post):
        source = post.find('div', attrs={'class': 'd_post_content j_d_post_content'})
        post_content = source.text
        post_id = post.attrs["data-pid"]
        floor_tail_info = post.find('div', attrs={'class': "post-tail-wrap"}).find_all('span', attrs={
            'class': 'tail-info'})
        public_device = ''
        floor_id = floor_tail_info[-2].text[:-1]  # 所处在的楼层
        publish_time = floor_tail_info[-1].text
        if len(floor_tail_info) == 3:
            public_device = floor_tail_info[0].text
        post_info = {
            "content": post_content,
            "publish_time": publish_time,
            "floor_id": floor_id,
            "public_device": public_device,
            "post_id": post_id,
        }
        return post_info

    def extract_reply(self, now_page):
        reply_data = self.request.get(
            self.request_reply_url.format(int(time.time() * 1000), self.topic_id, now_page)).json()
        if reply_data["errno"] != 0:
            print("get reply data raise error")
            comment_info = {}
        else:
            comment_info = reply_data["data"]["comment_list"]
        return comment_info

    def get_topic_info(self):
        soup_html = BeautifulSoup(self.request.get(
            url=self.request_url.format(self.topic_id, self.now_page)).content,
                                  features="html.parser")
        # 会员发的帖子需要在属性上增加 vip_red
        source = soup_html.find('h3', attrs='core_title_txt pull-left text-overflow') or \
                 soup_html.find('h3', attrs='core_title_txt pull-left text-overflow vip_red')
        try:
            topic_title = source.attrs['title']
        except Exception as e:
            topic_title = 'uncatch'
            spider_log.info("start crawl tieba topic:{}, title content uncatch".format(self.topic_id))

        topic_total_page_nums = int(soup_html.find('ul', attrs={'class': 'l_posts_num'})
                                    .find_all('li', attrs={'class': 'l_reply_num'})[0]
                                    .find_all('span')[1].text)
        self.topic_title = topic_title
        self.topic_total_page_nums = topic_total_page_nums

    def save_user(self, user_id, user_name, avatar, nickname):
        TiebaController.create_user(
            user_id=user_id,
            user_name=user_name,
            avatar=avatar,
            nickname=nickname
        )

    def save_post(self, topic_id, content, user_id, publish_time, floor_id, public_device, post_id):
        TiebaController.create_post(
            topic_id=topic_id, content=content, user_id=user_id,
            publish_time=publish_time, floor_id=floor_id, post_id=post_id,
            public_device=public_device, page=self.now_page
        )

    def save_reply(self, content, post_id, user_id, reply_id, reply_time, floor_id):
        TiebaController.create_reply(
            content=content,
            post_id=post_id,
            user_id=user_id,
            reply_id=reply_id,
            reply_time=reply_time,
            floor_id=floor_id,
        )

    def create_crawl_topic_status(self):
        url = self.request_url.format(self.topic_id, self.now_page)[:-1]  # 不保存页码
        TiebaController.create_topic_crawl(topic_id=self.topic_id, title=self.topic_title, crawl_page=self.now_page,
                                           url=url)

    def update_topic_crawl_status(self):
        TiebaController.update_topic_crawl(topic_id=self.topic_id, crawl_page=self.now_page)

    def run(self):

        self.get_topic_info()
        self.create_crawl_topic_status()
        # 检查是否爬取过， 从最新一页开始爬
        spider_task_info = TiebaController.get_topic_info_by_topic_id(self.topic_id)
        self.now_page = spider_task_info.get('crawl_page', 1)
        while self.now_page <= self.topic_total_page_nums:
            self.process_webpage()
            self.update_topic_crawl_status()
            self.now_page += 1
            time.sleep(self.crawl_interval)  # 避免爬的速度过快产生其他问题

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
