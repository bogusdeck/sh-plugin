# Generated by Django 5.1.2 on 2024-10-23 11:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_app', '0003_billingtokens_charge_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usage',
            name='usage_date',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
