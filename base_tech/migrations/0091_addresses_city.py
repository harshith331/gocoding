# Generated by Django 2.2.6 on 2020-04-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0090_addresses'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='city',
            field=models.CharField(default='roorkee', max_length=100),
            preserve_default=False,
        ),
    ]
