# Generated by Django 3.2.4 on 2021-11-25 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0045_order_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='shipping',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=30, null=True),
        ),
    ]