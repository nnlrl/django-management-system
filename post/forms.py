# !/usr/bin/python3
# @File: forms.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月10日DAY日11时
# 说明: 创建博客的表单
# 总结:

from django import forms
from django.forms import widgets


class PostForm(forms.Form):
    title = forms.CharField(label="标题", min_length=1, max_length=150,
                            widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "标题"}),
                            error_messages={"min_length": "标题不能小于1个字符",
                                            "max_length": "标题不能大于150个字符",
                                            "required": "标题不能为空"})
    introduction = forms.CharField(label="简介", min_length=1, max_length=150,
                                   widget=widgets.Textarea(
                                       attrs={"class": "form-control", "placeholder": "简介", "rows": 3}),
                                   error_messages={"min_length": "简介不能小于1个字符",
                                                   "max_length": "简介不能大于150个字符",
                                                   "required": "简介不能为空"})
    body = forms.CharField(label="主体内容",
                           widget=widgets.Textarea(attrs={"class": "form-control", "placeholder": "主体内容"}))
    is_open = forms.CharField(label="是否公开",
                              widget=widgets.CheckboxInput())
