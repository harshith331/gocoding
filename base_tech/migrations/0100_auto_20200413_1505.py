# Generated by Django 3.0.2 on 2020-04-13 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0099_addresses_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverying_boys_subs',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('C', 'Completed')], default='A', max_length=20),
        ),
    ]