# Generated by Django 3.1.6 on 2021-02-19 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210219_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermanagement',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_org', to='order.order'),
        ),
    ]
