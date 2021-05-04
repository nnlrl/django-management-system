# !/usr/bin/python3
# --coding:utf-8--
# @File   : urls.py
# @Author : nnlrl
# @Time   : 2021/2/22 13:23
# 说明     :
from django.urls import path
from . import views

urlpatterns = [
    path('delete/<int:comment_id>/', views.delete_view)
]