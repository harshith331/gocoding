# Generated by Django 3.0.2 on 2020-04-13 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_side', '0004_prev_orders_order_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='prev_orders',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
