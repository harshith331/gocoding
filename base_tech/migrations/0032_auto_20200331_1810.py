# Generated by Django 2.2.6 on 2020-03-31 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0031_auto_20200331_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='order_date',
        ),
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='order_time',
        ),
    ]