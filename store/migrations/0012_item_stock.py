# Generated by Django 3.2.4 on 2021-10-23 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_item_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='stock',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]