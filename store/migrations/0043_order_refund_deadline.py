# Generated by Django 3.2.4 on 2021-11-22 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_auto_20211122_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refund_deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
