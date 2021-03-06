# Generated by Django 3.1.6 on 2021-03-17 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0014_auto_20210310_1140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '订单管理', 'verbose_name_plural': '订单管理'},
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='ordermanagement',
            name='invoice',
            field=models.CharField(choices=[('不需要发票', '不需要发票'), ('个人发票', '个人发票'), ('内蒙古大学', '内蒙古大学')], default='内蒙古大学', max_length=20, verbose_name='发票信息'),
        ),
        migrations.AlterField(
            model_name='ordermanagement',
            name='payment_type',
            field=models.CharField(choices=[('线上支付', '线上支付'), ('货到付款', '货到付款')], default='线上支付', max_length=20, verbose_name='支付类型'),
        ),
        migrations.AlterModelTable(
            name='ordermanagement',
            table='订单处理',
        ),
    ]
