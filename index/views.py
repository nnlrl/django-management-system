from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime

from notifications.models import Notification

from post.models import Post
from order.models import Order


# u.order_set.exclude(status="closed").values("payment").aggregate(total=Sum("payment"))
# Create your views here.
# @cache_page(60 * 10)
@permission_required(["post.view_post", "order.view_order", "comment.view_comment"])
@login_required
def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.filter(is_active=True, is_open=True)
    my_posts = request.user.post_set.filter(is_active=True).count()
    comments = request.user.comment_set.filter(is_active=True)
    my_orders = request.user.order_set.exclude(status="closed")
    orders = Order.objects.exclude(status="closed").count()
    page, paginator, dis_range = split_page(posts.order_by("timestamp"), request, per_page=10)
    return render(request, "index/index.html", {"value": datetime.now(),
                                                "posts": posts,
                                                "my_posts": my_posts,
                                                "comments": comments,
                                                "orders": orders,
                                                "my_orders": my_orders,
                                                'page': page,
                                                'paginator': paginator,
                                                'dis_range': dis_range})


def notice_view(request: HttpRequest) -> HttpResponse:
    nid = request.GET.get("nid")
    ret_dict = {}
    if int(nid) != 0:
        try:
            notice = Notification.objects.get(id=nid)
            notice.unread = False
            notice.save()
            ret_dict["code"] = 200
        except:
            ret_dict["code"] = 404
    else:
        notices = request.user.notifications.unread()
        notices.mark_all_as_read()
        ret_dict["code"] = 200
    return JsonResponse(ret_dict)


def split_page(object_list, request, per_page=8):
    paginator = Paginator(object_list, per_page)
    # 取出当前需要展示的页码, 默认为1
    page_num = request.GET.get('page', default='1')
    # 根据页码从分页器中取出对应页的数据
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger as e:
        # 不是整数返回第一页数据
        page = paginator.page('1')
        page_num = 1
    except EmptyPage as e:
        # 当参数页码大于或小于页码范围时,会触发该异常
        print('EmptyPage:{}'.format(e))
        if int(page_num) > paginator.num_pages:
            # 大于 获取最后一页数据返回
            page = paginator.page(paginator.num_pages)
        else:
            # 小于 获取第一页
            page = paginator.page(1)

    # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
    page_num = int(page_num)
    if paginator.num_pages > 5:
        if page_num <= 2:
            dis_range = range(1, 6)
        elif page_num >= paginator.num_pages - 2:
            dis_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            dis_range = range(page_num - 2, page_num + 3)
    else:
        dis_range = paginator.page_range

    return page, paginator, dis_range
