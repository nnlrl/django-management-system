import datetime

from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Sum, Count
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect
from notifications.signals import notify
from django.db.models.functions import TruncDay

from .forms import *
from user.models import User
from djangoProject.email import send_mail


# Create your views here.
@permission_required("order.view_order")
def order_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_staff:
        orders = Order.objects.exclude(status="closed")
        orders_unprocessed = Order.objects.filter(status="unprocessed")
    else:
        orders = request.user.order_set.exclude(status="closed")
        orders_unprocessed = request.user.order_set.filter(status="unprocessed")

    return render(request, 'order/order.html', {"orders": orders,
                                                "orders_unprocessed": orders_unprocessed})


@permission_required(["order.add_order", "order.add_orderlogging"])
@login_required
def add_order_view(request: HttpRequest) -> HttpResponse:
    form = CreateOrderForm()
    if request.method == "POST":
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            order = Order(name=form.cleaned_data.get("name"),
                          kind=form.cleaned_data.get("kind"),
                          company=form.cleaned_data.get("company"),
                          unit_price=form.cleaned_data.get("unit_price"),
                          amount=form.cleaned_data.get("amount"),
                          payment=form.cleaned_data.get("payment"),
                          uinfo=form.cleaned_data.get("uinfo"),
                          user=request.user)
            order.save()

            log = OrderLogging(order=order,
                               user=request.user,
                               content=OrderLogging.CREATE)
            log.save()

            notify.send(sender=User.objects.filter(is_superuser=1).first(),
                        recipient=request.user,
                        verb="您已成功创建订单, 待管理员审核!")

            messages.info(request, "您已成功创建订单")
            return redirect('/order')

    return render(request, 'order/add_order.html', {"form": form})


@permission_required("is_staff")
def order_check_view(request: HttpRequest, order_id: int) -> HttpResponse:
    form = OrderManagementForm()
    try:
        order = Order.objects.get(id=order_id)
        logs = OrderLogging.objects.filter(order=order)
    except:
        messages.warning(request, "该订单不存在")
        return redirect("/order")
    if request.method == "POST":
        form = OrderManagementForm(request.POST)
        if form.is_valid():
            if int(form.cleaned_data.get("status")) == 2:
                order.status = Order.CLOSED
                order.save()

                messages.info(request, "该订单已成功关闭")
                return redirect('/order')
            else:
                order.status = Order.PROCESSED
                order.save()

                order_org = OrderManagement.objects.filter(order=order).first()
                if not order_org:
                    order_org = OrderManagement(order=order,
                                                unit_price1=form.cleaned_data.get("unit_price"),
                                                payment1=form.cleaned_data.get("payment"),
                                                # payment_type=form.cleaned_data.get("payment_type"),
                                                # invoice=form.cleaned_data.get("invoice"),
                                                # shipping_name=form.cleaned_data.get("shipping_name"),
                                                # shipping_code=form.cleaned_data.get("shipping_code"),
                                                ainfo=form.cleaned_data.get("ainfo"))
                    order_org.save()

                    log = OrderLogging(order=order,
                                       user=request.user,
                                       content=OrderLogging.PROCESS)
                    log.save()

                    notify.send(sender=request.user,
                                recipient=order.user,
                                verb="订单号为%s的订单已成功受理" % str(order.id))

                    messages.info(request, "订单已成功受理")
                else:
                    order_org.unit_price1 = form.cleaned_data.get("unit_price")
                    order_org.payment1 = form.cleaned_data.get("payment")
                    order_org.ainfo = form.cleaned_data.get("ainfo")

                    log = OrderLogging(order=order,
                                       user=request.user,
                                       content=OrderLogging.PROCESS)
                    log.save()

                    notify.send(sender=request.user,
                                recipient=order.user,
                                verb="订单号为%s的订单的受理细节已经修改" % str(order.id))

                    messages.info(request, "修改成功")
                if form.cleaned_data.get("send_mail") == "True":
                    context = {"username": order.user.username,
                               "manager": request.user.username,
                               "status": order.status,
                               "id": order.id,
                               "name": order.name,
                               "unit_price": order.unit_price,
                               "amount": order.amount,
                               "payment": order.payment,
                               "ainfo": order.order_org.ainfo,
                               "uinfo": order.uinfo}
                    send_mail(subject="您的订单已受理", body="email/status_change.html", to=order.user.email,
                              context=context)
                return redirect('/order')
    return render(request, 'order/order_check.html', {"form": form,
                                                      "order": order,
                                                      "logs": logs})


@login_required
def order_delete_view(request: HttpRequest, order_id: int) -> HttpResponse:
    if request.user.is_staff:
        order = Order.objects.get(id=order_id)
    else:
        try:
            order = Order.objects.get(id=order_id)
            assert order.user == request.user
        except:
            messages.warning(request, "订单不存在或者尝试修改他人订单")
            return redirect('/order')

    order.status = "closed"
    order.save()
    messages.info(request, "您已成功关闭该订单")

    if request.user.is_staff and order.user != request.user:
        notify.send(sender=request.user,
                    recipient=order.user,
                    verb="订单号为%s的订单已被管理员%s关闭" % (str(order.id), request.user.username))

    return redirect('/order')


@login_required
@permission_required(["order.view_order", "order.add_orderlogging"])
def edit_order_view(request: HttpRequest, order_id: int) -> HttpResponse:
    if request.user.is_staff:
        order = Order.objects.get(id=order_id)
        logs = OrderLogging.objects.filter(order=order)
    else:
        try:
            order = Order.objects.get(id=order_id)
            assert order.user == request.user
            logs = OrderLogging.objects.filter(order=order)
        except:
            messages.warning(request, "订单不存在或者尝试修改他人订单")
            return redirect('/order')
    form = CreateOrderForm(initial={"name": order.name,
                                    "company": order.company,
                                    "unit_price": order.unit_price,
                                    "amount": order.amount,
                                    "payment": order.payment,
                                    "uinfo": order.uinfo})
    if order.status != "unprocessed":
        messages.warning(request, "该订单已完成, 不能修改")
        return redirect('/order')
    if request.method == "POST":
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order.name = form.cleaned_data.get("name")
            order.company = form.cleaned_data.get("company")
            order.unit_price = form.cleaned_data.get("unit_price")
            order.amount = form.cleaned_data.get("amount")
            order.payment = form.cleaned_data.get("payment")
            order.uinfo = form.cleaned_data.get("uinfo")
            order.save()

            log = OrderLogging(order=order, content=OrderLogging.UPDATE)
            log.save()

            messages.info(request, "订单已成功修改")

            if request.user.is_staff and order.user != request.user:
                notify.send(sender=request.user,
                            recipient=order.user,
                            verb="订单号为%s的订单已被管理员%s修改" % (str(order.id), request.user.username))

            return redirect('/order')

    return render(request, 'order/edit_order.html', {"form": form,
                                                     "logs": logs,
                                                     "order": order})


@login_required
def order_statistics_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_staff:
        all_users = User.objects.all()
        return render(request, "order/order_statistics.html",
                      {"all_users": all_users})
    return render(request, "order/order_statistics.html")


@login_required
def order_statistics_ajax(request: HttpRequest, userid: str) -> HttpResponse:
    if request.is_ajax():
        try:
            user = User.objects.get(userid=userid)
        except:
            messages.warning(request, "用户不存在")
            return redirect("/order/")

        def get_orders(type):
            # 筛选前两周的订单
            last_two_weeks = datetime.datetime.now().date() - datetime.timedelta(weeks=2)
            if type == "all":
                orders = user.order_set.exclude(status="closed").filter(create_time__gte=last_two_weeks)
            else:
                orders = user.order_set.filter(status=type).filter(create_time__gte=last_two_weeks)

            count = list(
                orders.annotate(day=TruncDay("create_time")).values("day").annotate(count=Sum("payment")).values(
                    "count"))
            stack = 0
            stack_count = []
            for i in range(len(count)):
                stack += count[i].get("count")
                stack_count.append(float(stack))
            all_count = [float(i["count"]) for i in count]

            # 获取时间节点, 用于横坐标展示
            timestamp_query = list(
                orders.annotate(day=TruncDay("create_time")).values("day").annotate(count=Count("id")).values("day"))
            all_times = [i["day"].strftime("%m-%d") for i in timestamp_query]

            # 获取每一种类的订单金额, 用于柱状图和饼状图展示
            all_kinds_query = list(
                user.order_set.exclude(status="closed").values("kind").annotate(count=Sum("payment")))
            all_kinds = [i["kind"] for i in all_kinds_query]
            kinds_count = [float(i["count"]) for i in all_kinds_query]

            return {"timestamp": all_times,
                    "all_count": all_count,
                    "stack_count": stack_count,
                    "all_kinds": all_kinds,
                    "kinds_count": kinds_count}

        last_one_year = datetime.datetime.now().date() - datetime.timedelta(days=365)
        all_orders_count = user.order_set.exclude(status="closed").filter(create_time__gte=last_one_year).count()
        all_orders_payment = user.order_set.exclude(status="closed").filter(create_time__gte=last_one_year).aggregate(
            Sum("payment")).get("payment__sum")
        processed_orders_count = user.order_set.filter(status="processed").filter(
            create_time__gte=last_one_year).count()
        unprocessed_orders_count = user.order_set.filter(status="unprocessed").filter(
            create_time__gte=last_one_year).count()

        res = {"code": 200,
               "data": {
                   "all": get_orders("all"),
                   "processed": get_orders("processed"),
                   "unprocessed": get_orders("unprocessed"),
                   "all_orders_count": all_orders_count,
                   "all_orders_payment": all_orders_payment / 10000,
                   "processed_orders_count": processed_orders_count,
                   "unprocessed_orders_count": unprocessed_orders_count,
               }
               }
        return JsonResponse(res)
    return JsonResponse({"code": 403})


@permission_required("is_staff")
def order_statistics_admin_ajax(request: HttpRequest, userid: str) -> HttpResponse:
    if request.is_ajax():
        try:
            user = User.objects.get(userid=userid)
            return order_statistics_ajax(request, user.userid)
        except:
            messages.warning(request, "用户不存在")
            return redirect("/order/")
    return JsonResponse({"code": 403})
