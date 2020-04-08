# Generated by Django 2.2.6 on 2020-03-31 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0035_subscribed_orders_completion_status'),
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
        migrations.AlterField(
            model_name='subscribed_orders',
            name='delivery_dates',
            field=models.CharField(default='11', max_length=200),
        ),
        migrations.AlterField(
            model_name='subscribed_orders',
            name='delivery_time',
            field=models.CharField(default='11', max_length=200),
        ),
        migrations.AlterField(
            model_name='subscribed_orders',
            name='duration',
            field=models.CharField(default='1', max_length=50),
        ),
    ]