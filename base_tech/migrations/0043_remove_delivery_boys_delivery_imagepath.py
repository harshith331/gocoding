# Generated by Django 2.2.6 on 2020-04-01 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0042_delivery_boys_delivery_imagepath'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery_boys',
            name='delivery_imagepath',
        ),
    ]
