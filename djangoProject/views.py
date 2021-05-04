# !/usr/bin/python3
# @File: views.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月09日DAY日20时
# 说明: 
# 总结:
from django.shortcuts import render


def page_not_found_404(request, exception):
    # 返回错误码
    error_code = "404"
    return render(request, "404.html", {
        "error_code": error_code
    })


def system_error_500(request):
    error_code = "500"
    return render(request, "500.html", {
        "error_code": error_code,
    })
