# Generated by Django 3.1.6 on 2021-02-13 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body_html',
            field=models.TextField(default='', verbose_name='内容(html)'),
        ),
    ]
