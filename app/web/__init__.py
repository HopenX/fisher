# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 5:39 AM
# @Author  : Hopen

from flask import Blueprint, render_template

web = Blueprint('web', __name__)  # 蓝图名称，蓝图所在的模块


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from app.web import book  # 导入才能 @web.route 注册
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
