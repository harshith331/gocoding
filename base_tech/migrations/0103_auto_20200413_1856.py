# Generated by Django 3.0.2 on 2020-04-13 13:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0102_auto_20200413_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribed_orders',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime.now),
        ),
    ]
