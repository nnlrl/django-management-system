# Generated by Django 3.1.6 on 2021-02-10 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about_me',
            field=models.CharField(default='', max_length=150, verbose_name='about me'),
        ),
        migrations.AddField(
            model_name='user',
            name='education',
            field=models.CharField(default='', max_length=150, verbose_name='education'),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(default='', max_length=150, verbose_name='location'),
        ),
    ]
