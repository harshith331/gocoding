# Generated by Django 3.0.2 on 2020-04-13 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0112_auto_20200413_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='start_date',
        ),
    ]
