# Generated by Django 3.0.2 on 2020-02-08 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0004_auto_20200206_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='iteminfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_no', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='vendors',
            name='items',
            field=models.IntegerField(default=0),
        ),
    ]
