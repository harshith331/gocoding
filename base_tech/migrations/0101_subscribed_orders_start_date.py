# Generated by Django 3.0.2 on 2020-04-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0100_auto_20200413_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribed_orders',
            name='start_date',
            field=models.DateField(default=1),
            preserve_default=False,
        ),
    ]
