# !/usr/bin/python3
# @File: email.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月08日DAY日22时
# 说明: 发送邮件
# 总结:

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader
from threading import Thread


def send_async_mail(msg):
    msg.send()


def send_mail(subject, body, to, **kwargs):
    body = loader.render_to_string(body, context=kwargs["context"])
    msg = EmailMessage(subject=subject, body=body, to=[to])
    msg.content_subtype = "html"
    thr = Thread(target=send_async_mail, args=[msg])
    thr.start()
    # msg.send()
    return thr
