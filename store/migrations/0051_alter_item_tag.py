# Generated by Django 3.2.4 on 2021-11-28 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0050_remove_orderitem_old_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tag',
            field=models.CharField(blank=True, choices=[('S', 'sale'), ('N', 'new'), ('L', 'limited'), ('O', 'out')], default='N', max_length=1, null=True),
        ),
    ]
