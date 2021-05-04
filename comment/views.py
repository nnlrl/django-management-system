from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from notifications.signals import notify


# Create your views here.
@permission_required("is_superuser")
def delete_view(request: HttpRequest, comment_id: int) -> HttpResponse:
    try:
        comment = Comment.objects.get(id=comment_id, is_active=True)
    except:
        messages.warning(request, "此评论不存在, 请重新输入")

        return redirect('/post')
    comment.is_active = False
    notify.send(sender=request.user,
                recipient=comment.author,
                verb="您对文章《%s》的评论已被管理员%s删除" % (comment.post.title, request.user.username))
    return redirect('/post/%s' % comment.post_id)