# Generated by Django 2.2.6 on 2020-04-03 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0056_auto_20200403_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresses',
            name='id',
        ),
        migrations.AddField(
            model_name='addresses',
            name='address_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
