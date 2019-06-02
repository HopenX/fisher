# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 12:16 AM
# @Author  : Hopen

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, desc, func
from app.models.base import Base, db
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook
from flask import current_app
from collections import namedtuple

EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])  # 快速定义对象的方法


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13), nullable=False)
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)
        ).all()
        return gifts

    @classmethod
    def get_wishes_count(cls, isbn_list):
        """
        :param isbn_list: isbn 的列表
        :return: 到 Wish 表中查询出某个礼物的 wish 心愿数量
        和 filter_by 不同. 能用查询语句写，尽量就不要用 python 处理. 不要直接返回，否则 count_list[0][1] 可读性差
        """
        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    def is_yourself_gift(self, uid):
        if self.uid == uid:
            return True

    @classmethod
    def recent(cls):
        recent_gift = cls.query.filter_by(launched=False).order_by(
            desc(Gift.create_time)).group_by(Gift.isbn).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gift

# group_by 和 distinct 配合去重  order_by 应该在 group_by 前面
# 链式调用
# 主体 Query
# 子函数
# first() all()
