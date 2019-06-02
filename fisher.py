# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 1:44 AM
# @Author  : Hopen

from app import creat_app

app = creat_app()

if __name__ == '__main__':
    # 生产环境 Nginx+uwsgi
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
