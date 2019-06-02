# -*- coding: utf-8 -*-
# @Time    : 2019/5/24 10:10 PM
# @Author  : Hopen
from threading import Thread

from app import mail
from flask_mail import Message
from flask import current_app, render_template


# 异步发送邮件
def send_async_email(app, msg):
    with app.app_context():  # 不加这句话，会有异常 work outside
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    # msg = Message('测试邮件', sender='1152214965@qq.com', body='Test', recipients=['1152214965@qq.com'])

    msg = Message('「鱼书」' + ' ' + subject, sender=current_app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    true_app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[true_app, msg])
    thr.start()

    # 若使用：thr = Thread(target=send_async_email, args=[current_app, msg])
    """
    # 这里传递的是一个代理对象，不是一个真实的 Flask 核心对象
    # 代理的对象去查找 Flask 核心对象的时候，是根据线程 id 进行查找
    # 而真是的对象在任何的线程中都是存在的
    """
