# Generated by Django 3.1.6 on 2021-03-10 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_open',
            field=models.BooleanField(default=True, verbose_name='是否公开'),
        ),
    ]
