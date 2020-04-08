# Generated by Django 2.2.6 on 2020-04-05 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0091_addresses_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendors_subs',
            name='vendor_status',
            field=models.CharField(choices=[('D', 'Delivered'), ('N', 'Not Delivered')], default='N', max_length=20),
        ),
    ]
