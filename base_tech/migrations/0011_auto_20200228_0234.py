# Generated by Django 3.0.2 on 2020-02-27 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0010_auto_20200225_0416'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_items',
            name='otp',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('D', 'Delivered'), ('A', 'Active')], default='A', max_length=50),
        ),
        migrations.AddField(
            model_name='orders',
            name='primary_vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base_tech.Vendors'),
        ),
        migrations.AddField(
            model_name='vendors',
            name='money_earned',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vendors',
            name='penalty_money',
            field=models.IntegerField(default=0),
        ),
    ]