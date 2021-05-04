# !/usr/bin/python3
# @File: fun_filter.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月10日DAY日11时
# 说明: 
# 总结:

import hashlib

from django import template

register = template.Library()


@register.filter()  # 使用这个装饰器
def gravatar(user, size=100, default='identicon', rating='g'):
    # 国内cdn加速
    url = "https://sdn.geekzu.org/avatar"
    hash = hashlib.md5(user.email.encode("utf-8")).hexdigest()
    return f"{url}/{hash}?s={size}&d={default}&r={rating}". \
        format(url=url, hash=hash, size=size, default=default, rating=rating)
