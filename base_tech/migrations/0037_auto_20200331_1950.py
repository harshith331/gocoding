# Generated by Django 2.2.6 on 2020-03-31 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0036_auto_20200331_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery_boys',
            name='delivery_imagepath',
        ),
        migrations.RemoveField(
            model_name='vendors',
            name='vendor_imagepath',
        ),
    ]
