# Generated by Django 3.1.6 on 2021-04-15 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_auto_20210317_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermanagement',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='ordermanagement',
            name='payment_type',
        ),
        migrations.RemoveField(
            model_name='ordermanagement',
            name='shipping_code',
        ),
        migrations.RemoveField(
            model_name='ordermanagement',
            name='shipping_name',
        ),
        migrations.AddField(
            model_name='ordermanagement',
            name='payment1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='折后总价'),
        ),
        migrations.AddField(
            model_name='ordermanagement',
            name='unit_price1',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='折后单价'),
        ),
        migrations.AlterField(
            model_name='ordermanagement',
            name='order',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='order_org', to='order.order'),
        ),
    ]
