# Generated by Django 3.1.6 on 2021-02-19 03:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount',
            field=models.IntegerField(default=1, verbose_name='商品数量'),
        ),
        migrations.AddField(
            model_name='ordermanagement',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='操作时间'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ordermanagement',
            name='ainfo',
            field=models.TextField(blank=True, verbose_name='管理员备注'),
        ),
    ]