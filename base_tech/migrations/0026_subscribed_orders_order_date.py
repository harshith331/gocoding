# Generated by Django 3.0.2 on 2020-03-26 18:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0025_auto_20200326_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribed_orders',
            name='order_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
