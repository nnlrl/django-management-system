# Generated by Django 3.1.6 on 2021-02-08 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210208_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Confirmed'),
        ),
    ]