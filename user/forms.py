# !/usr/bin/python3
# @File: forms.py
# --coding:utf-8--
# @Author: nnlrl
# @Time: 2021年02月06日DAY日21时
# 说明: 用户权限表单
# 总结:


from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.forms import widgets


class LoginForm(forms.Form):
    userid = forms.CharField(label="学号",
                             min_length=8, max_length=8,
                             widget=widgets.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "请输入学生id"}),
                             error_messages={"min_length": "请输入8位学号",
                                             "max_length": "请输入8位学号",
                                             "required": "学号不能为空"})
    email = forms.EmailField(label="邮箱",
                             widget=widgets.EmailInput(attrs={"class": "form-control",
                                                              "placeholder": "请输入邮箱"}),
                             error_messages={"required": "请输入正确的邮箱格式",
                                             "invalid": "请输入正确的邮箱格式"})
    password = forms.CharField(label="密码", min_length=1, max_length=64,
                               widget=widgets.PasswordInput(attrs={"class": "form-control",
                                                                   "placeholder": "请输入密码"}),
                               error_messages={"required": "密码不能为空",
                                               "min_length": "密码不能小于1个字符",
                                               "max_length": "密码不能大于64个字符"})

    captcha = CaptchaField(label="验证码", widget=CaptchaTextInput(attrs={"class": "form-control",
                                                                       "placeholder": "验证码"}))


class RegisterForm(forms.Form):
    userid = forms.CharField(label="学号",
                             min_length=8, max_length=8,
                             widget=widgets.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "请输入学号"}),
                             error_messages={"min_length": "请输入8位学号",
                                             "max_length": "请输入8位学号",
                                             "required": "学号不能为空"})
    username = forms.CharField(label="姓名",
                               max_length=150, min_length=1,
                               widget=widgets.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "请输入姓名"}),
                               error_messages={"min_length": "姓名不能小于1个字符",
                                               "max_length": "姓名不能大于150个字符",
                                               "required": "姓名不能为空"})
    email = forms.EmailField(label="邮箱",
                             max_length=150, min_length=1,
                             widget=widgets.EmailInput(attrs={"class": "form-control",
                                                              "placeholder": "请输入邮箱"}),
                             error_messages={"min_length": "邮箱不能小于1个字符",
                                             "max_length": "邮箱不能大于150个字符",
                                             "required": "邮箱不能为空",
                                             "invalid": "请输入正确的邮箱格式"})
    password1 = forms.CharField(label="密码",
                                max_length=150, min_length=1,
                                widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入密码"}),
                                error_messages={"min_length": "密码不能小于1个字符",
                                                "max_length": "密码不能大于150个字符",
                                                "required": "密码不能为空"})
    password2 = forms.CharField(label="密码确认",
                                max_length=150, min_length=1,
                                widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请再次输入密码"}),
                                error_messages={"min_length": "密码不能小于1个字符",
                                                "max_length": "密码不能大于150个字符",
                                                "required": "密码不能为空"})

    captcha = CaptchaField(label="验证码", widget=CaptchaTextInput(attrs={"class": "form-control",
                                                                       "placeholder": "验证码"}))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次密码不匹配, 请重新输入!")
        return password2


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label="邮箱", max_length=150, min_length=1,
                             widget=widgets.EmailInput(attrs={"class": "form-control", "readonly": ''}),
                             error_messages={"min_length": "邮箱不能小于1个字符",
                                             "max_length": "邮箱不能大于150个字符",
                                             "required": "邮箱不能为空",
                                             "invalid": "请输入正确的邮箱格式"})
    password0 = forms.CharField(label="原密码", min_length=1, max_length=150,
                                widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入原密码"}),
                                error_messages={"min_length": "密码不能小于1个字符",
                                                "max_length": "密码不能大于150个字符",
                                                "required": "密码不能为空"})
    password1 = forms.CharField(label="输入新密码", min_length=1, max_length=150,
                                widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入新密码"}),
                                error_messages={"min_length": "密码不能小于1个字符",
                                                "max_length": "密码不能大于150个字符",
                                                "required": "密码不能为空"})
    password2 = forms.CharField(label="密码确认", min_length=1, max_length=150,
                                widget=widgets.PasswordInput(
                                    attrs={"class": "form-control", "placeholder": "请再次输入新密码"}),
                                error_messages={"min_length": "密码不能小于1个字符",
                                                "max_length": "密码不能大于150个字符",
                                                "required": "密码不能为空"})
    captcha = CaptchaField(label="验证码", widget=CaptchaTextInput(attrs={"class": "form-control"}))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次密码不匹配, 请重新输入!")
        return password2


class ForgetPasswordForm(forms.Form):
    userid = forms.CharField(label="学号", min_length=8, max_length=8,
                             widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入学号"}),
                             error_messages={"min_length": "请输入8位学生id",
                                             "max_length": "请输入8位学生id",
                                             "required": "学号不能为空"})
    email = forms.CharField(label="邮箱", min_length=1, max_length=150,
                            widget=widgets.EmailInput(attrs={"class": "form-control", "placeholder": "请输入邮箱"}),
                            error_messages={"min_length": "邮箱不能小于1个字符",
                                            "max_length": "邮箱不能大于150个字符",
                                            "required": "邮箱不能为空",
                                            "invalid": "请输入正确的邮箱格式"})
    username = forms.CharField(label="姓名", min_length=1, max_length=150,
                               widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入姓名"}),
                               error_messages={"min_length": "姓名不能小于1个字符",
                                               "max_length": "姓名不能大于150个字符",
                                               "required": "姓名不能为空"})

    captcha = CaptchaField(label="验证码", widget=CaptchaTextInput(attrs={"class": "form-control",
                                                                       "placeholder": "验证码"}))


class ForgetPasswordForm2(forms.Form):
    password1 = forms.CharField(label="请输入新密码", min_length=1, max_length=150,
                                widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请输入新密码"}),
                                error_messages={"min_length": "密码不能小于1个字符",
                                                "max_length": "密码不能大于150个字符",
                                                "required": "密码不能为空"})
    password2 = forms.CharField(label="密码确认", min_length=1, max_length=150,
                                widget=widgets.PasswordInput(attrs={"class": "form-control", "placeholder": "请再次输入密码"}),
                                error_messages={"min_length": "密码不能小于1个字符",
                                                "max_length": "密码不能大于150个字符",
                                                "required": "密码不能为空"})
    captcha = CaptchaField(label="验证码", widget=CaptchaTextInput(attrs={"class": "form-control",
                                                                       "placeholder": "验证码"}))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次密码不匹配, 请重新输入!")
        return password2


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="邮箱",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', "class": "form-control", "placeholder": "请输入邮箱"})
    )


class MySetPasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': "两次密码不匹配, 请重新输入",
    }
    new_password1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control',
                                          'placeholder': '请输入新密码'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="密码确认",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control',
                                          'placeholder': '请重复输入新密码'
                                          }))

    def clean_new_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次密码不匹配, 请重新输入!")
        return password2


class UserInfoForm(forms.Form):
    username = forms.CharField(label="用户名", min_length=1, max_length=150, required=False,
                               widget=widgets.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "用户名"}),
                               error_messages={"min_length": "用户名不能小于1个字符",
                                               "max_length": "用户名不能大于150个字符",
                                               "required": "用户名不能为空"})

    education = forms.CharField(label="教育经历", min_length=1, max_length=150, required=False,
                                widget=widgets.TextInput(attrs={"class": "form-control",
                                                                "placeholder": "教育经历"}),
                                error_messages={"min_length": "学校不能小于1个字符",
                                                "max_length": "学校不能大于150个字符"})

    address = forms.CharField(label="住址", min_length=1, max_length=150, required=False,
                              widget=widgets.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "现住址"}),
                              error_messages={"min_length": "住址不能小于1个字符",
                                              "max_length": "住址不能大于150个字符"})
    about_me = forms.CharField(label="简介", min_length=1, max_length=150, required=False,
                               widget=widgets.Textarea(attrs={"class": "form-control",
                                                              "placeholder": "简介",
                                                              "rows": 3}),
                               error_messages={"min_length": "简介不能小于1个字符",
                                               "max_length": "简介不能大于150个字符"})
