# Generated by Django 3.2.4 on 2021-10-10 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_item_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tag',
            field=models.CharField(choices=[('S', 'sale'), ('N', 'new'), ('L', 'limited')], max_length=1, null=True),
        ),
    ]