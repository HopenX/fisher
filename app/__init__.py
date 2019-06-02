# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 5:36 AM
# @Author  : Hopen

from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')  # 使用配置
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    db.create_all(app=app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    mail.init_app(app)
    # 或者
    # with app.app_context():
    #     db.create_all()
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
