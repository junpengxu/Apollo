# -*- coding: utf-8 -*-
# @Time    : 2020/10/18 9:31 上午
# @Author  : xu.junpeng

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, BaseQuery


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(is_delete=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.is_delete else None


db = SQLAlchemy(use_native_unicode='utf8mb4', query_class=QueryWithSoftDelete)


class BaseModel(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)
    is_delete = db.Column(db.Boolean, default=False)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise e

    def update(self):
        try:
            db.session.merge(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise e

    @staticmethod
    def save_all(model_list):
        try:
            db.session.add_all(model_list)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise e
