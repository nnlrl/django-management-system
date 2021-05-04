from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, Http404, JsonResponse
from django.shortcuts import render, redirect
from notifications.signals import notify

from comment.forms import *
from comment.models import *
from .forms import *
from user.models import *


# Create your views here.
@permission_required("post.add_post")
@login_required
def add_view(request: HttpRequest) -> HttpResponse:
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        print(form.data)
        if form.is_valid():
            try:
                post = Post(author=request.user,
                            title=form.cleaned_data.get("title"),
                            introduction=form.cleaned_data.get("introduction"),
                            body=form.cleaned_data.get("body"),
                            body_html=Post.to_html(form.cleaned_data.get("body")),
                            is_open=True if form.cleaned_data.get("is_open") else False)
                post.save()
                notify.send(
                    sender=request.user,
                    actor=User.objects.get(is_superuser=1),
                    recipient=request.user,
                    verb='文章《%s》已经成功发布！' % post.title,
                )
                messages.info(request, "文章发布成功")
                return redirect('/post/%d' % post.id)
            except Exception as e:
                print(str(e))
                messages.warning(request, str(e))
    return render(request, "post/add_post.html", {"form": form})


@permission_required(["post.view_post", "comment.add_comment"])
@login_required
def post_view(request: HttpRequest, pid: int) -> HttpResponse:
    try:
        post = Post.objects.get(id=pid, is_active=True)
        form = CommentForm()
        paginator = Paginator(post.comment_set.filter(is_active=True).order_by("timestamp"), 5)
        count = paginator.count
        try:
            page = int(request.GET.get(key='page', default='1'))
            comments = paginator.get_page(page)
        except PageNotAnInteger:
            comments = paginator.get_page(1)
        except EmptyPage:
            comments = paginator.get_page(1)

        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment(body=form.cleaned_data.get("body"),
                                  post=post,
                                  author=request.user,
                                  body_html=Comment.to_html(form.cleaned_data.get("body")))
                comment.save()

                notify.send(sender=request.user,
                            recipient=post.author,
                            verb="%s评论了您的文章:《%s》" % (request.user.username, post.title))

                messages.info(request, "评论已经发布")

                return redirect('/post/view_post')
        return render(request, 'post/view_post.html', {"post": post,
                                                       "form": form,
                                                       "comments": comments,
                                                       "count": count})
    except Exception as e:
        print(str(e))
        messages.warning(request, str(e))
    return render(request, 'index/index.html')


@permission_required("post.view_post")
@login_required
def edit_view(request: HttpRequest, post_id: int) -> HttpResponse:
    post = Post.objects.filter(id=post_id, is_active=True).first()
    if post:
        if request.user != post.author and not request.user.is_staff:
            return HttpResponseForbidden()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post.body = form.cleaned_data.get("body")
                post.introduction = form.cleaned_data.get("introduction")
                post.title = form.cleaned_data.get("title")
                post.body_html = Post.to_html(form.cleaned_data.get("body"))
                post.save()
                messages.info(request, "文章已成功修改")

        form = PostForm(initial={"title": post.title,
                                 "introduction": post.introduction})
        if request.user == post.author and request.user.is_staff:
            notify.send(sender=request.user,
                        recipient=post.author,
                        verb="管理员%s修改了您的文章:《%s》" % (request.user.username, post.title))

        return render(request, "post/edit_post.html", {"form": form,
                                                       "post": post})
    else:
        raise Http404()


@permission_required("post.view_post")
@login_required
def likes_view(request: HttpRequest) -> HttpResponse:
    resp = {}
    if request.is_ajax():
        post_id = request.GET.get("post_id")
        action = request.GET.get("action")
        if post_id and action:
            try:
                post = Post.objects.get(id=post_id, is_active=True)
                users = post.likes.all()
                if action == '1':
                    # 对点赞进行操作
                    if request.user not in users:
                        post.likes.add(request.user)
                        post.save()
                        resp["is_liked"] = True
                        resp["code"] = 200
                        notify.send(sender=request.user,
                                    recipient=post.author,
                                    verb="用户%s赞了您的文章:《%s》" % (request.user.username, post.title))
                    else:
                        post.likes.remove(request.user)
                        post.save()
                        resp["is_liked"] = False
                        resp["code"] = 200
                else:
                    # 首次进入文章详情页获取点赞数
                    if request.user not in users:
                        resp["is_liked"] = False
                        resp["code"] = 200
                        resp["total_like"] = len(users)
                    else:
                        resp["is_liked"] = True
                        resp["code"] = 200
                        resp["total_like"] = len(users)
            except Exception as e:
                print(str(e))
                resp["is_liked"] = None
                resp["code"] = 500
            return JsonResponse(resp)
    else:
        return HttpResponseForbidden()


@permission_required(["post.view_post", "post.add_post"])
@login_required
def share_post_view(request: HttpRequest, post_id: int) -> HttpResponse:
    if request.is_ajax():
        try:
            post = Post.objects.get(id=post_id, is_active=True)
        except:
            messages.warning(request, "该文章不存在")
            return redirect("/user/%s" % str(request.user.userid))
        content = post.introduction + "  --转载至 %s" % post.author.username
        new_post = Post(title=post.title,
                        introduction=content,
                        body=post.body,
                        body_html=post.body_html,
                        author=request.user)
        new_post.save()

        notify.send(sender=request.user,
                    recipient=post.author,
                    verb="用户%s转发了您的文章:《%s》" % (request.user.username, post.title))

        messages.info(request, "文章转载成功")
        return redirect("/user/%s" % str(request.user.userid))
    return render(request, "/")


@login_required
def delete_view(request: HttpRequest, post_id: int) -> HttpResponse:
    if request.is_ajax():
        if request.user.is_staff:
            post = Post.objects.get(id=post_id, is_active=True)
        else:
            try:
                post = Post.objects.get(id=post_id, is_active=True)
                assert post.author == request.user
            except:
                messages.warning(request, "此文章不存在, 请重新输入")
                return JsonResponse({"code": 404})
        post.is_active = False
        post.save()
        if request.user.is_staff and post.author != request.user:
            notify.send(sender=request.user,
                        recipient=post.author,
                        verb="文章《%s》已被管理员%s删除" % (post.title, request.user.username))
        messages.info(request, "文章已成功删除")
        return JsonResponse({"code": 200})
    else:
        return HttpResponseForbidden()


@permission_required("post.view_post")
@login_required
def all_view(request: HttpRequest) -> HttpResponse:
    all_posts = request.user.post_set.filter(is_active=True).order_by("timestamp")
    paginator = Paginator(all_posts, 10)
    try:
        page = int(request.GET.get(key='page', default='1'))
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(1)
    return render(request, 'post/all_posts.html', {"posts": posts})
