# Generated by Django 3.0.2 on 2020-02-19 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paytm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RazorPay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ORDERID', models.CharField(max_length=30, verbose_name='ORDER ID')),
                ('razorpay_order_id', models.CharField(max_length=70)),
                ('razorpay_payment_id', models.CharField(max_length=70)),
            ],
        ),
    ]