# Generated by Django 3.2.4 on 2021-10-23 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_item_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.item'),
        ),
    ]