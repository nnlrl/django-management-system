from django.contrib import admin

from django import forms

# Register your models here.
from .models import Order, OrderManagement, OrderLogging


# TODO: ModelForm添加外键内容
class OrderAdminInline(admin.StackedInline):
    model = OrderManagement


# class OrderLoggingInline(admin.TabularInline):
#     model = OrderLogging


class OrderAdmin(admin.ModelAdmin):
    list_display = ["name", "kind", "unit_price", "amount", "payment", "status", "user",
                    "_userid", "_unit_price1", "_payment1", "create_time", "update_time"]
    fieldsets = [
        (None, {'fields': ['name', 'kind']}),
        ('价格信息', {'fields': ['unit_price', 'amount', 'payment']}),
        ('状态信息', {'fields': ['status']}),
        ('创建者', {'fields': ['user']}),
        ('备注信息', {'fields': ['uinfo']}),
    ]
    list_editable = ('status',)
    search_fields = ('user__username',)
    list_filter = ('status', 'create_time', 'kind', 'order_org__unit_price1',
                   'order_org__payment1')
    inlines = [OrderAdminInline]

    def _userid(self, obj):
        return obj.user.userid

    def _unit_price1(self, obj):
        return obj.order_org.unit_price1

    def _payment1(self, obj):
        return obj.order_org.payment1


admin.site.register(Order, OrderAdmin)
