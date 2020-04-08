# Generated by Django 2.2.6 on 2020-04-04 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0069_delete_vendors_subs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendors_subs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sorder_id', models.CharField(max_length=500)),
                ('order_date', models.DateField(auto_now_add=True, verbose_name='Order date')),
                ('order_time', models.TimeField(auto_now_add=True, verbose_name='Order time')),
                ('vendor_status', models.CharField(choices=[('D', 'Delivered'), ('N', 'Not Delivered')], default='D', max_length=20)),
                ('otp', models.IntegerField(blank=True, default=0)),
                ('phone_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_tech.Vendors')),
            ],
        ),
    ]
