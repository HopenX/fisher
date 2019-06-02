# -*- coding: utf-8 -*-
# @Time    : 2019/5/4 3:07 AM
# @Author  : Hopen

import requests


# urllib or requests 发送http请求
class HTTP:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
