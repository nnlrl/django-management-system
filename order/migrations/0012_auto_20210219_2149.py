# Generated by Django 3.1.6 on 2021-02-19 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20210219_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlogging',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]