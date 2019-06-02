# -*- coding: utf-8 -*-
# @Time    : 2019/5/23 2:24 AM
# @Author  : Hopen

from collections import namedtuple

from app.view_models.book import BookViewModel


class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.gifts = self.__parse()

    def __parse(self):
        """
        :return: 字典的列表, 作为 gifts 属性
        """
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        """
        :param gift: 就是 Model 里的 Gift
        :return:
        """
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book),
            'id': gift.id
        }
        return r

# MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])
# my_gift = MyGift(gift.id, BookViewModel(gift.book), count)  # 形成一个单独的视图：书 & 数量
# 字典比对象好用
