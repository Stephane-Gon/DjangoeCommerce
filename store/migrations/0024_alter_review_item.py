# Generated by Django 3.2.4 on 2021-10-30 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_rename_review_review_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.item'),
        ),
    ]
