# Generated by Django 3.2.4 on 2021-12-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0061_alter_transaction_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='replica',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
