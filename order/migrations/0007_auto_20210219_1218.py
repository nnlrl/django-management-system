# Generated by Django 3.1.6 on 2021-02-19 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210219_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermanagement',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processed', '已处理'), ('unprocessed', '未处理'), ('closed', '已关闭')], default='unprocessed', max_length=20, verbose_name='订单状态'),
        ),
    ]