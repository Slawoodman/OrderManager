# Generated by Django 4.2.2 on 2023-07-05 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("market", "0009_alter_orderitem_address_alter_orderitem_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_item",
                to="market.product",
            ),
        ),
    ]
