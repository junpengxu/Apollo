# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 12:27 下午
# @Author  : xu.junpeng
from app.models.tieba import BaiduTiebaReply, BaiduTiebaTopic, BaiduTiebaUser


class TiebaController:

    def create_user(self, user_id, user_name, avatar, user_nickname):
        try:
            user = BaiduTiebaUser(user_id=user_id, user_name=user_name, avatar=avatar, user_nickname=user_nickname)
            user.save()
        except:
            return False

    def create_topic(self, topic_id, content, user_id, floor_id, publish_time, public_device):
        try:
            topic = BaiduTiebaTopic(
                topic_id=topic_id, content=content, user_id=user_id, floor_id=floor_id, publish_time=publish_time,public_device=public_device
            )
            topic.save()
        except:
            return False

    def create_reply(self, content, user_id, floorid, reply_time, reply_user_id):
        try:
            reply = BaiduTiebaReply(
                user_id=user_id, content=content, floorid=floorid, reply_time=reply_time, reply_user_id=reply_user_id
            )
            reply.save()
        except:
            return False
