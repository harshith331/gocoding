# Generated by Django 2.2.6 on 2020-04-04 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0080_delete_addresses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('address_id', models.IntegerField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=350)),
                ('pincode', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('category', models.CharField(max_length=100)),
                ('phone_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_tech.RegUser')),
            ],
        ),
    ]
