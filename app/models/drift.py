# -*- coding: utf-8 -*-
# @Time    : 2019/5/25 6:54 PM
# @Author  : Hopen

from app.libs.enums import PendingStatus
from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.models.base import Base


class Drift(Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'drift'

    def __init__(self):
        self.pending = PendingStatus.Waiting.value
        super(Drift, self).__init__()

    # 交易信息
    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    pending = Column(Integer, default=1)  # 鱼漂的状态

    # 可以更优雅
    # @property
    # def pending(self):
    #     return PendingStatus(self.pending)
    #
    # @pending.setter
    # def pending(self, status):
    #     self.pending = status.value
