# -*- coding: utf-8 -*-
# @Time    : 2020/11/12 9:30 下午
# @Author  : xu.junpeng

from app import celery
from app.utils.logger import spider_log
from app.utils.spider_utils.crawl_tieba import Crawl


@celery.task
def run_zongyue_tieba_spider(topic_id, start_page, end_page):
    spider_log.info("start crawl tieba topic:{}, start page:{}, end_page:{}".format(topic_id, start_page, end_page))
    spider = Crawl(topic_id, start_page, end_page)
    spider.run()
    spider_log.info("finish crawl tieba topic:{}, start page:{}, end_page:{}".format(topic_id, start_page, end_page))
