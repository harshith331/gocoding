# Generated by Django 2.2.6 on 2020-04-04 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0076_auto_20200404_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='house_no',
            field=models.IntegerField(default=0),
        ),
    ]