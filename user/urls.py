# !/usr/bin/python3
# @File: urls.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月06日DAY日18时
# 说明: 
# 总结:

from django.contrib.auth import views as views_
from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/user/login
    path('login/', views.login_view),
    # 127.0.0.1:8000/user/logout
    path('logout/', views.logout_view),
    # 127.0.0.1:8000/user/register
    path('register/', views.register_view),
    # 127.0.0.1:8000/user/unconfirmed
    path('unconfirmed/', views.unconfirmed_view),
    # 127.0.0.1:8000/user/confirm/<token>
    path('confirm/<str:token>', views.confirm_view),
    # 127.0.0.1:8000/user/confirm/<token>
    path('confirm/', views.resend_view),
    # 127.0.0.1:8000/user/change-password
    path('change-password/', views.reset_password_view),
    # 127.0.0.1:8000/user/refresh_captcha
    path('refresh_captcha/', views.refresh_captcha_view),
    # 127.0.0.1:8000/user/password-reset
    path('password-reset/',
         views.CustomPasswordResetView.as_view(),
         name="password_reset"),
    # 127.0.0.1:8000/user/password-reset/done/
    path('password-reset/done/',
         views_.PasswordResetDoneView.as_view(template_name="user/forget_password2.html"),
         name="password_reset_done"),
    # 127.0.0.1:8000/user/reset/<uidb64>/<token>/
    path('reset/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    # 127.0.0.1:8000/user/reset/done/
    path('reset/done/',
         views_.PasswordResetCompleteView.as_view(template_name="user/forget_password4.html"),
         name="password_reset_complete"),
    # 127.0.0.1:8000/user/<userid>
    path('<str:userid>/', views.user_view)
]
