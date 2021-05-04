# Generated by Django 3.1.6 on 2021-02-19 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0007_auto_20210219_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderLogging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(choices=[('create', '创建订单'), ('update', '修改订单'), ('delete', '删除订单')], default='create', max_length=6, verbose_name='操作内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '订单日志',
                'verbose_name_plural': '订单日志',
            },
        ),
    ]