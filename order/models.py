from django.db import models
from django.conf import settings

# Create your models here.
from django.utils import timezone


class Order(models.Model):
    CLOSED = "closed"
    UNPROCESSED = "unprocessed"
    PROCESSED = "processed"
    STATUS_CHOICE = ((PROCESSED, "已处理"), (UNPROCESSED, "未处理"), (CLOSED, "已关闭"))

    name = models.CharField(verbose_name="商品名称", max_length=150)
    kind = models.CharField(verbose_name="商品种类", max_length=150, default="其他")
    amount = models.IntegerField(verbose_name="商品数量", default=1)
    company = models.CharField(verbose_name="公司名称", max_length=150)
    unit_price = models.DecimalField(verbose_name="商品单价", max_digits=10, decimal_places=2)
    payment = models.DecimalField(verbose_name="订单金额", max_digits=10, decimal_places=2)

    create_time = models.DateTimeField(verbose_name="订单创建日期", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="订单更新日期", auto_now=True)
    status = models.CharField(verbose_name="订单状态", choices=STATUS_CHOICE,
                              default=UNPROCESSED, max_length=20)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="创建者")
    uinfo = models.TextField(verbose_name="备注信息", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name


class OrderManagement(models.Model):
    unit_price1 = models.DecimalField(verbose_name="折后单价", max_digits=10, decimal_places=2)
    payment1 = models.DecimalField(verbose_name="折后总价", max_digits=10, decimal_places=2)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="order_org")
    ainfo = models.TextField(verbose_name="管理员备注", blank=True)
    timestamp = models.DateTimeField(verbose_name="操作时间", auto_now_add=True)

    class Meta:
        db_table = "订单处理"
        verbose_name = "订单处理"
        verbose_name_plural = verbose_name


class OrderLogging(models.Model):
    CREATE = "create"
    UPDATE = "update"
    PROCESS = "process"
    DELETE = "delete"
    CONTENT_CHOICE = ((CREATE, "创建订单"), (UPDATE, "修改订单"), (DELETE, "删除订单"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    content = models.CharField(verbose_name="操作内容", max_length=20, choices=CONTENT_CHOICE,
                               default=CREATE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "订单日志"
        verbose_name_plural = verbose_name
