# Generated by Django 5.1.1 on 2024-09-19 05:31

import shopify_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_app', '0002_client_custom_frequency_in_hours_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientcollections',
            name='parameters_used',
            field=models.JSONField(default=shopify_app.models.default_parameters_used),
        ),
    ]
