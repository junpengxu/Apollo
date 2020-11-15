# -*- coding: utf-8 -*-
# @Time    : 2020/11/8 12:27 下午
# @Author  : xu.junpeng
from app.models.tieba import BaiduTiebaReply, BaiduTiebaPost, BaiduTiebaUser, BaiduTiebaTopic


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
                                  topic_id=topic_id, content=content, user_id=user_id, floor_id=floor_id,
                                  publish_time=publish_time, public_device=public_device
                                  )
            post.save()
        except:
            return False

    @classmethod
    def create_reply(cls, content, user_id, floor_id, reply_time, reply_id, post_id):
        try:
            reply = BaiduTiebaReply(
                user_id=user_id, content=content, floor_id=floor_id, reply_time=reply_time, reply_id=reply_id,
                post_id=post_id
            )
            reply.save()
        except:
            return False

    @classmethod
    def create_topic(cls, topic_id, title, url, crawl_page):
        try:
            topic = BaiduTiebaTopic(
                title=title, topic_id=topic_id, crawl_page=crawl_page, url=url
            )
            topic.save()
        except:
            return False

    @classmethod
    def update_topic_crawl_status(cls, topic_id, crawl_page):
        try:
            topic = BaiduTiebaTopic.query.filter_by(topic_id=topic_id).first()  # 根据unique的限制，应该只能获取出一条数据
            topic.crawl_page = crawl_page
            topic.save()
        except:
            return False

    @classmethod
    def get_posts_by_topic_id(cls, topic_id, page, offset):
        posts = BaiduTiebaPost.query.filter_by(topic_id=topic_id).order_by(BaiduTiebaPost.post_id.desc()).paginate(
            page=page, per_page=offset, error_out=False).items
        result = [{
            "content": post.content, "device": post.public_device, "post_id": post.post_id,
            "user_id": post.user_id, "floor_id": post.floor_id, "publish_time": post.publish_time
        } for post in posts]
        total_nums = BaiduTiebaPost.query.filter_by(topic_id=topic_id).count()
        return {"result": result, "total_nums": total_nums}

    @classmethod
    def get_reply_by_posts(cls, post_ids):
        replys = BaiduTiebaReply.query.filter(BaiduTiebaReply.post_id.in_(post_ids)).all()
        result = {
            reply.reply_id: {
                "content": reply.content,
                "user_id": reply.user_id,
                "floor_id": reply.floor_id,
                "reply_time": reply.reply_time,
                "post_id": reply.post_id,
            } for reply in replys
        }
        return result

    @classmethod
    def get_user_info_by_user_ids(cls, user_ids):
        users = BaiduTiebaUser.query.filter(BaiduTiebaUser.user_id.in_(user_ids)).all()
        result = {
            user.user_id: {
                "user_name": user.user_name,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "user_id": user.user_id,
            } for user in users
        }
        return result
