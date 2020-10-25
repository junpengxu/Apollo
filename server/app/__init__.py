# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 1:00 上午
# @Author  : xu.junpeng

from app.admin.urls import bind_urls
import os
from flask import Flask
from app.base.basemodel import db

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object("config")

db.init_app(app)

bind_urls(app)

# if you want create database table;
# you should run `flask shell` in terminal at Apollo, and then do this
# 1. from app.admin.models import *
# 2. from app import db
# 3. db.create_all()
