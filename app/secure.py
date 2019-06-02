# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 2:05 AM
# @Author  : Hopen

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:987654321@localhost:3306/fisher'
# 也可以连接分布式数据库

SECRET_KEY = '\x88D\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJ:U\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x98*4'

# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '1152214965@qq.com'
MAIL_PASSWORD = 'igljzfvjkswmhaae'
# MAIL_SUBJECT_PREFIX = '[鱼书]'
MAIL_SENDER = '1152214965@qq.com'
