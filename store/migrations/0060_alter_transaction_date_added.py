# Generated by Django 3.2.4 on 2021-12-16 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0059_transaction_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_added',
            field=models.DateTimeField(),
        ),
    ]
