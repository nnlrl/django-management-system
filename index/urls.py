# !/usr/bin/python3
# @File: urls.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月06日DAY日18时
# 说明: 
# 总结:
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('notice/', views.notice_view),
]
