# Generated by Django 2.2.6 on 2020-04-01 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0041_vendors_vendor_imagepath'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_boys',
            name='delivery_imagepath',
            field=models.ImageField(default='toys.png', upload_to='images/'),
        ),
    ]