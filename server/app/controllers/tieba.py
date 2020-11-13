# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 12:27 下午
# @Author  : xu.junpeng
from app.models.tieba import BaiduTiebaReply, BaiduTiebaPost, BaiduTiebaUser


class TiebaController:

    @classmethod
    def create_user(cls, user_id, user_name, avatar, nickname):
        try:
            user = BaiduTiebaUser(user_id=user_id, user_name=user_name, avatar=avatar, nickname=nickname)
            user.save()
        except:
            return False

    @classmethod
    def create_post(cls, topic_id, post_id, content, user_id, floor_id, publish_time, public_device):
        try:
            post = BaiduTiebaPost(post_id=post_id,
                topic_id=topic_id, content=content, user_id=user_id, floor_id=floor_id, publish_time=publish_time,public_device=public_device
            )
            post.save()
        except:
            return False

    @classmethod
    def create_reply(cls, content, user_id, floor_id, reply_time, reply_id, post_id):
        try:
            reply = BaiduTiebaReply(
                user_id=user_id, content=content, floor_id=floor_id, reply_time=reply_time,reply_id=reply_id, post_id=post_id
            )
            reply.save()
        except:
            return False
