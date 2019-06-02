# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 3:58 AM
# @Author  : Hopen

from flask import jsonify, request, render_template, flash
from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from flask_login import current_user
import json

from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    # q = request.args['q']  # 从Form中取值更好
    # page = request.args['page']  # Immutable不可变字典, request 几乎包含所有 http 请求信息，可以解析问号

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
        # 函数式编程，权限交给调用方，比如 sorted filter
    else:
        # return jsonify(form.errors)
        flash('搜索的关键字不存在')
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_wishes = False
    has_in_gifts = False
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)

    # 取得详情数据，并渲染到模板中
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        # 如果未登录，current_user将是一个匿名用户对象
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,  # 自己的 filter_by 函数
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    # 传出：book BookViewModel 类型，gifts wishes 都是 TradeInfo 类型
    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
