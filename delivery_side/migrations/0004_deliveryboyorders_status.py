# Generated by Django 2.2.6 on 2020-04-05 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_side', '0003_remove_deliveryboyorders_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboyorders',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('D', 'Delivered')], default='A', max_length=20),
        ),
    ]
