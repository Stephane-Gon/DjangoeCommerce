# Generated by Django 3.2.4 on 2021-11-26 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0047_alter_item_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3),
        ),
    ]
