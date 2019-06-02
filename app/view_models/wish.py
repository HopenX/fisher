# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 2:14 PM
# @Author  : Hopen

from app.view_models.book import BookViewModel


class MyWishes:
    """
    自己的心愿列表，并包含有多少人愿意送的列表
    """
    def __init__(self, wishes_of_mine, gift_count_list):
        self.wishes = []
        self.__wishes_of_mine = wishes_of_mine
        self.__gift_count_list = gift_count_list
        self.wishes = self.__parse()

    def __parse(self):
        """
        :return: 字典的列表, 作为 wishes 属性
        """
        temp_wishes = []
        for wish in self.__wishes_of_mine:
            my_wish = self.__matching(wish)
            temp_wishes.append(my_wish)
        return temp_wishes

    def __matching(self, wish):
        """
        :param wish: 自己的一个 wish
        :return: 能匹配多少的 gift，记录书本id 和对应数量
        """
        count = 0
        for gift_count in self.__gift_count_list:
            if wish.isbn == gift_count['isbn']:
                count = gift_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(wish.book),
            'id': wish.id
        }
        return r