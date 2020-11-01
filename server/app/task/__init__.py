# -*- coding: utf-8 -*-
# @Time    : 2020/11/1 11:49 上午
# @Author  : xu.junpeng

from celery import Celery
from config import BROKER_URL


def make_celery(app):
    celery = Celery('Apollo', broker=BROKER_URL)
    celery.config_from_object('celery_config')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
