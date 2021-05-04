# !/usr/bin/python3
# @File: urls.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月10日DAY日11时
# 说明: 
# 总结:


from django.urls import path, include
from . import views


urlpatterns = [
    # 127.0.0.1:8000/post/
    path('', views.all_view),
    # 127.0.0.1:8000/post/add-post/
    path('add-post/', views.add_view),
    # 127.0.0.1:8000/post/<post_id>
    path('<int:pid>/', views.post_view),
    # 127.0.0.1:8000/post/edit/<post_id>
    path('edit/<int:post_id>/', views.edit_view),
    # 127.0.0.1:8000/post/edit/<post_id>
    path('delete/<int:post_id>/', views.delete_view),
    # 127.0.0.1:8000/post/like/
    path('like/', views.likes_view),
    # 127.0.0.1:8000/post/share/<post_id>
    path('share/<int:post_id>/', views.share_post_view),
]
