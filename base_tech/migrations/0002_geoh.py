# Generated by Django 3.0.2 on 2020-02-06 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='geoh',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geoh', models.CharField(max_length=12)),
            ],
        ),
    ]
