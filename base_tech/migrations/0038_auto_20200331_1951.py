# Generated by Django 2.2.6 on 2020-03-31 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0037_auto_20200331_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_boys',
            name='delivery_imagepath',
            field=models.ImageField(default='default.jpg', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='vendors',
            name='vendor_imagepath',
            field=models.ImageField(default='default.jpg', upload_to='images/'),
        ),
    ]
