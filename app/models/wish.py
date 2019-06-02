# -*- coding: utf-8 -*-
# @Time    : 2019/5/20 2:51 PM
# @Author  : Hopen

from app.spider.yushu_book import YuShuBook
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, func, desc
from sqlalchemy.orm import relationship
from app.models.base import Base, db


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)
        ).all()
        return wishes

    @classmethod
    def get_gifts_count(cls, isbn_list):
        """
        :param isbn_list: isbn 的列表
        :return: 到 Gift 表中查询出某个礼物的 gift 数量
        和 filter_by 不同. 能用查询语句写，尽量就不要用 python 处理. 不要直接返回，否则 count_list[0][1] 可读性差
        """
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list
