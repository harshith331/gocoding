# Generated by Django 3.0.2 on 2020-02-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0006_auto_20200219_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='geohash_distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geohash1', models.CharField(max_length=50)),
                ('geohash2', models.CharField(max_length=50)),
                ('dist', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='cells',
            name='Cell_products',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Vendor_Products',
        ),
    ]
