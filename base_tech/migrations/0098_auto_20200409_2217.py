# Generated by Django 3.0.2 on 2020-04-09 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0097_auto_20200409_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_boys',
            name='parking_no',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_items',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
