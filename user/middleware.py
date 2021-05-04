# !/usr/bin/python3
# @File: middleware.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月09日DAY日00时
# 说明: 中间件
# 总结:
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class MyMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest):
        if request.user.is_authenticated and not request.user.confirmed \
                and not request.get_full_path().startswith("/static") \
                and not request.get_full_path().startswith("/user") \
                and not request.get_full_path().startswith("/captcha"):
           return redirect("/user/unconfirmed")
