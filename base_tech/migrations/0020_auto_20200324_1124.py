# Generated by Django 3.0.2 on 2020-03-24 05:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0019_order_items_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='vendor_phone',
        ),
        migrations.AddField(
            model_name='orders',
            name='price',
            field=models.IntegerField(default=50),
        ),
        migrations.CreateModel(
            name='Subscribed_Order_Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sorder_id', models.CharField(default=uuid.uuid4, max_length=100)),
                ('quantity', models.IntegerField()),
                ('size', models.FloatField(default=1)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base_tech.CategorizedProducts')),
                ('vendor_phone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='base_tech.Vendors')),
            ],
        ),
    ]