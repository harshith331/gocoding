# Generated by Django 2.2.6 on 2020-04-03 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0060_auto_20200403_1516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addresses',
            old_name='address_ids',
            new_name='address_id',
        ),
    ]
