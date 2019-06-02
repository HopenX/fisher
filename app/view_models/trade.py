# -*- coding: utf-8 -*-
# @Time    : 2019/5/22 9:45 PM
# @Author  : Hopen
from app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, goods):
        # 接收的 goods 即为 Wish 或 Gift 类型，传出 trades 为字典类型
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )


# 可读性很差的重构
# class MyTrades:
#     def __init__(self, trades_of_mine, trade_count_list):
#         self.trades = []
#         self.__trades_of_mine = trades_of_mine
#         self.__trade_count_list = trade_count_list
#         self.trades = self.__parse()
#
#     def __parse(self):
#         """
#         :return: 字典的列表, 作为 trades 属性
#         """
#         temp_trades = []
#         for trade in self.__trades_of_mine:
#             my_trade = self.__matching(trade)
#             temp_trades.append(my_trade)
#         return temp_trades
#
#     def __matching(self, trade):
#         count = 0
#         for trade_count in self.__trade_count_list:
#             if trade.isbn == trade_count['isbn']:
#                 count = trade_count['count']
#         r = {
#             'trades_count': count,
#             'book': BookViewModel(trade.book),
#             'id': trade.id
#         }
#         return r
