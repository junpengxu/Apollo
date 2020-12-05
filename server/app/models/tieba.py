# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 10:58 上午
# @Author  : xu.junpeng

from app.base.basemodel import BaseModel, db


class BaiduTiebaPost(db.Model, BaseModel):
    __tablename__ = 'baidu_tieba_post'

    id = db.Column(db.BIGINT, primary_key=True)
    topic_id = db.Column(db.BIGINT, index=True)
    post_id = db.Column(db.BIGINT, unique=True)
    content = db.Column(db.String(4096), comment="发布内容")
    public_device = db.Column(db.String(64), comment="发布使用的设备")
    user_id = db.Column(db.BIGINT, comment="用户id")
    floor_id = db.Column(db.Integer, comment="楼层id")
    page = db.Column(db.Integer, comment="页码")
    publish_time = db.Column(db.DateTime, comment="创建时间")


class BaiduTiebaReply(db.Model, BaseModel):
    __tablename__ = 'baidu_tieba_reply'

    id = db.Column(db.BIGINT, primary_key=True)
    reply_id = db.Column(db.BIGINT, comment="回复id", unique=True)
    content = db.Column(db.String(4096), comment="回复内容")
    user_id = db.Column(db.BIGINT, comment="用户id")
    floor_id = db.Column(db.Integer, comment="回复的楼层id")
    reply_time = db.Column(db.DateTime, comment="创建时间")
    post_id = db.Column(db.BIGINT, comment="帖子id")


class BaiduTiebaTopic(db.Model, BaseModel):
    __tablename__ = 'baidu_tieba_topic'

    id = db.Column(db.BIGINT, primary_key=True)
    topic_id = db.Column(db.BIGINT, comment="帖子id", unique=True)
    title = db.Column(db.String(4096), comment="帖子title")
    url = db.Column(db.String(256), comment="帖子链接")
    user_id = db.Column(db.BIGINT, comment="用户id")
    crawl_page = db.Column(db.Integer, comment="爬取到的最新页码")


class BaiduTiebaUser(db.Model, BaseModel):
    __tablename__ = 'baidu_tieba_user'

    id = db.Column(db.BIGINT, primary_key=True)
    user_id = db.Column(db.BIGINT, comment="用户id", unique=True)
    user_name = db.Column(db.String(64), comment="用户名称")
    nickname = db.Column(db.String(64), comment="用户昵称")
    avatar = db.Column(db.String(256), comment="用户头像")
