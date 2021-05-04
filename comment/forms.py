# !/usr/bin/python3
# @File: forms.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月13日DAY日19时
# 说明: 
# 总结:


from django import forms
from django.forms import widgets


class CommentForm(forms.Form):
    body = forms.CharField(label="评论", min_length=1, max_length=150,
                                   widget=widgets.TextInput(
                                       attrs={"class": "form-control", "placeholder": "评论"}),
                                   error_messages={"min_length": "评论不能小于1个字符",
                                                   "max_length": "评论不能大于150个字符"})
