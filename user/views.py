import json

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, redirect
from notifications.signals import notify

from djangoProject.email import send_mail
from .forms import *
from .models import User


class CustomPasswordResetView(views.PasswordResetView):
    template_name = 'user/forget_password.html'
    form_class = MyPasswordResetForm


class CustomPasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'user/forget_password3.html'
    form_class = MySetPasswordForm


# Create your views here.
def login_view(request: HttpRequest) -> HttpResponse:
    form = LoginForm()
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data.get("userid"),
                                email=form.cleaned_data.get("email"),
                                password=form.cleaned_data.get("password"))
            if user:
                login(request, user)
                resp = redirect('/')
                return resp
        messages.warning(request, "用户名或密码错误, 请重新输入")

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')

    return render(request, "user/login.html", {"form": form,
                                               "hashkey": hashkey,
                                               "image_url": image_url})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, "您已成功退出!")
    return redirect('/')


def register_view(request: HttpRequest) -> HttpResponse:
    form = RegisterForm()
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(userid=form.cleaned_data.get("userid"))
                messages.warning(request, "用户已存在, 请重新输入")
            except:
                try:
                    if form.cleaned_data.get("password1") != form.cleaned_data.get("password2"):
                        raise ValueError("两次输入的密码必须一致")
                    # 尚未确认的user实例
                    user = User.objects.create_user(userid=form.cleaned_data.get("userid"),
                                                    email=form.cleaned_data.get("email"),
                                                    username=form.cleaned_data.get("username"),
                                                    password=form.cleaned_data.get("password1"))
                    login(request, user)
                    token = user.generate_confirm_token()
                    absurl = "http://" + request.META["HTTP_HOST"] + '/user/confirm/' + token
                    context = {"absurl": absurl,
                               "username": request.user.username}
                    send_mail(subject="注册确认", body="email/confirm.html", to=request.user.email,
                              context=context)
                    messages.info(request, "一封待确认的邮件已经发送到指定邮箱, 请查看")
                    return redirect('/')
                except Exception as e:
                    messages.warning(request, str(e))
    return render(request, "user/register.html", {"form": form,
                                                  "hashkey": hashkey,
                                                  "image_url": image_url})


# 尚未确认的用户可以查看的界面
@login_required
def unconfirmed_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_anonymous or request.user.confirmed:
        return redirect("/")
    else:
        return render(request, "user/unconfirmed.html")


# 进入该界面, 如果token匹配则激活并跳转到主页
@login_required
def confirm_view(request: HttpRequest, token: str) -> HttpResponse:
    if request.user.confirmed:
        return redirect('/')
    if request.user.confirm_token(token):
        request.user.save()

        notify.send(sender=User.objects.get(is_superuser=1),
                    recipient=request.user,
                    verb="恭喜您, 您已成功激活账号")

        messages.info(request, "您已经成功激活该账号, 谢谢")
        return redirect('/')
    else:
        messages.warning(request, "该链接已失效, 请重试")
    return redirect('/')


# 重发邮件
@login_required
def resend_view(request: HttpRequest) -> HttpResponse:
    token = request.user.generate_confirm_token()
    absurl = "http://" + request.META["HTTP_HOST"] + '/user/confirm/' + token
    context = {"absurl": absurl, "username": request.user.username}
    send_mail(subject="注册确认", body="email/confirm.html", to=request.user.email, context=context)
    messages.info(request, "一封新的待确认邮件已经发送到指定邮箱, 请及时查看")
    return redirect('/')


# 重置密码
@login_required
def reset_password_view(request: HttpRequest) -> HttpResponse:
    form = ResetPasswordForm(initial={"email": request.user.email})
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data.get("password0")) and \
                    form.cleaned_data.get("password1") == form.cleaned_data.get("password2"):
                request.user.set_password(form.cleaned_data.get("password1"))
                request.user.save()
                logout(request)
                messages.info(request, "密码已重置成功, 请重新登录")
                return redirect("/user/login")

    return render(request, "user/reset_password.html", {"form": form,
                                                        "hashkey": hashkey,
                                                        "image_url": image_url})


def refresh_captcha_view(request: HttpRequest) -> HttpResponse:
    """  Return json with new captcha for ajax refresh request """
    if not request.is_ajax():
        raise Http404

    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {"hashkey": hashkey, "image_url": image_url}

    return HttpResponse(json.dumps(captcha), content_type='application/json')


@login_required
def user_view(request: HttpRequest, userid: str) -> HttpResponse:
    if request.user.is_authenticated:
        orders = len(request.user.order_set.all())
        orders_unprocessed = len(request.user.order_set.filter(status="unprocessed"))
        form = UserInfoForm()
        try:
            user = User.objects.get(userid=userid, is_active=True)
            form = UserInfoForm(initial={"username": user.username,
                                         "education": user.education,
                                         "address": user.location,
                                         "about_me": user.about_me})
        except:
            raise Http404()
        paginator = Paginator(user.post_set.filter(is_active=True).order_by("timestamp"), 10)
        try:
            page = int(request.GET.get(key='page', default='1'))
            posts = paginator.get_page(page)
        except PageNotAnInteger:
            posts = paginator.get_page(1)
        except EmptyPage:
            posts = paginator.get_page(1)
        if not user:
            raise Http404
        if request.method == "POST":
            form = UserInfoForm(request.POST)
            if form.is_valid() and user.userid == request.user.userid:
                print(request.user.userid)
                request.user.username = form.cleaned_data.get("username")
                request.user.education = form.cleaned_data.get("education")
                request.user.location = form.cleaned_data.get("address")
                request.user.about_me = form.cleaned_data.get("about_me")
                request.user.save()
                messages.info(request, "用户信息以成功修改")
                return redirect("/")

        return render(request, "user/user.html", {"posts": posts,
                                                  "user": user,
                                                  "form": form,
                                                  "orders": orders,
                                                  "orders_unprocessed": orders_unprocessed})
    else:
        messages.warning(request, "请先登录")
        return render(request, "index/index.html")
