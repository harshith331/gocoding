# Generated by Django 3.0.2 on 2020-04-12 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_side', '0003_remove_prev_orders_nos'),
    ]

    operations = [
        migrations.AddField(
            model_name='prev_orders',
            name='order_type',
            field=models.CharField(choices=[('N', 'Normal'), ('S', 'Subscribed')], default='N', max_length=20),
        ),
    ]
