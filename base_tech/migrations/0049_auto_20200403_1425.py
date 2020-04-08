# Generated by Django 2.2.6 on 2020-04-03 14:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0048_auto_20200403_1423'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresses',
            name='id',
        ),
        migrations.AddField(
            model_name='addresses',
            name='address_id',
            field=models.IntegerField(default=datetime.datetime(2020, 4, 3, 14, 25, 19, 302232, tzinfo=utc), primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
