# !/usr/bin/python3
# --coding:utf-8--
# @File   : forms.py
# @Author : nnlrl
# @Time   : 2021/2/18 21:16
# 说明     :

from django import forms
from django.forms import widgets
from .models import *


class CreateOrderForm(forms.Form):
    name = forms.CharField(label="商品名称", min_length=1, max_length=150,
                           widget=widgets.TextInput(attrs={"class": "form-control",
                                                           "placeholder": "商品名称"}),
                           error_messages={"required": "商品名称不能为空",
                                           "min_length": "商品名称不能小于1个字符",
                                           "max_length": "商品名称不能超过150个字符"})
    kind = forms.CharField(label="商品种类",
                           widget=widgets.Select(choices=[("抗体", "抗体"), ("小分子", "小分子"),
                                                          ("消耗品", "消耗品"), ("培养液", "培养液"),
                                                          ("测序", "测序"), ("其他", "其他")],
                                                 attrs={"class": "form-control"}),
                           error_messages={"required": "商品名称不能为空",
                                           "min_length": "商品名称不能小于1个字符",
                                           "max_length": "商品名称不能超过150个字符"})
    company = forms.CharField(label="公司名称", min_length=1, max_length=150,
                              widget=widgets.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "公司名称"}),
                              error_messages={"required": "公司名称不能为空",
                                              "min_length": "公司名称不能小于1个字符",
                                              "max_length": "公司名称不能超过150个字符"})
    unit_price = forms.DecimalField(label="商品单价", min_value=0, max_digits=10, decimal_places=2,
                                    widget=widgets.TextInput(attrs={"class": "form-control",
                                                                    "placeholder": "商品单价"}),
                                    error_messages={"required": "单价不能为空",
                                                    "invalid": "请输入正确的单价格式",
                                                    "min_value": "单价不能小于0",
                                                    "max_digits": "单价不能超过10位数",
                                                    "max_decimal_places": "仅支持两位小数"})
    amount = forms.IntegerField(label="数量", max_value=999, min_value=1,
                                widget=widgets.TextInput(attrs={"class": "form-control",
                                                                "placeholder": "商品数量"}),
                                error_messages={"required": "单价不能为空",
                                                "invalid": "请输入整数数量",
                                                "min_value": "商品数量不能小于1个",
                                                "max_value": "商品数量不能大于999个"})
    payment = forms.DecimalField(label="订单金额", min_value=0, max_digits=10, decimal_places=2,
                                 widget=widgets.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "订单金额",
                                                                 "readonly": ''}),
                                 error_messages={"required": "金额不能为空",
                                                 "invalid": "请输入正确的金额格式",
                                                 "min_value": "金额不能小于0",
                                                 "max_digits": "金额不能超过10位数",
                                                 "max_decimal_places": "仅支持两位小数"})
    uinfo = forms.CharField(label="备注", max_length=300, min_length=1, required=False,
                            widget=widgets.Textarea(attrs={"class": "form-control",
                                                           "placeholder": "用户备注信息",
                                                           "rows": 3}),
                            error_messages={"min_length": "备注信息不能小于0个字符",
                                            "max_length": "备注信息不能大于300个字符"})


class OrderManagementForm(forms.Form):
    status = forms.CharField(label="订单状态",
                             widget=widgets.RadioSelect(choices=[(1, "同意"), (2, "拒绝")],
                                                        ))
    unit_price = forms.DecimalField(label="折后单价", min_value=0, max_digits=10, decimal_places=2,
                                    widget=widgets.TextInput(attrs={"class": "form-control",
                                                                    "placeholder": "折后单价"}),
                                    error_messages={"required": "单价不能为空",
                                                    "invalid": "请输入正确的单价格式",
                                                    "min_value": "单价不能小于0",
                                                    "max_digits": "单价不能超过10位数",
                                                    "max_decimal_places": "仅支持两位小数"})
    payment = forms.DecimalField(label="折后总价", min_value=0, max_digits=10, decimal_places=2,
                                 widget=widgets.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "折后总价"}),
                                 error_messages={"required": "金额不能为空",
                                                 "invalid": "请输入正确的金额格式",
                                                 "min_value": "金额不能小于0",
                                                 "max_digits": "金额不能超过10位数",
                                                 "max_decimal_places": "仅支持两位小数"})
    ainfo = forms.CharField(label="管理员备注", required=False,
                            widget=widgets.Textarea(attrs={"class": "form-control",
                                                           "rows": 3,
                                                           "placeholder": "管理员备注信息"}))
    send_mail = forms.CharField(label="是否发送邮件",
                                widget=widgets.CheckboxInput())
