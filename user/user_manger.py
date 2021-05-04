# !/usr/bin/python3
# @File: user_manger.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月08日DAY日21时
# 说明: 自定义Manager管理器
# 总结:
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, userid: str, username: str, password: str, email: str, **kwargs):
        if not userid or len(userid) != 8:
            raise ValueError("请输入有效的八位学生id")
        if not username:
            raise ValueError("请输入用户名")
        if not password:
            raise ValueError("请输入密码")
        if not email or '@' not in email:
            raise ValueError("请输入有效的邮箱格式")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **kwargs)
        user.userid = userid
        user.set_password(password)
        user.save()
        return user

    def create_staff(self, userid: str, username: str, password: str, email: str, **kwargs):  # 创建普通用户
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = True
        user = self._create_user(userid, username, password, email, **kwargs)
        user.groups.add(2)
        return user

    def create_user(self, userid: str, username: str, password: str, email: str, **kwargs):  # 创建普通用户
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = False
        user = self._create_user(userid, username, password, email, **kwargs)
        user.groups.add(1)
        return user

    def create_superuser(self, userid: str, username: str, password: str, email: str, **kwargs):  # 创建超级用户
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(userid, username, password, email, **kwargs)
