# Generated by Django 2.2.1 on 2019-08-17 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0003_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Buyer.Address', verbose_name='订单地址'),
        ),
    ]
