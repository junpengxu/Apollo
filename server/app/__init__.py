# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:00 上午
# @Author  : xu.junpeng
import os
from flask import Flask
from app.base.basemodel import db

from celery import Celery

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config.from_object("config")
db.init_app(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)


def create_app():
    from app.urls import bind_urls
    bind_urls(app)
    return app

# if you want create database table;
# you should run `flask shell` in terminal at Apollo, and then do this
# 1. from app.admin.models import *
# 2. from app import db
# 3. db.create_all()
