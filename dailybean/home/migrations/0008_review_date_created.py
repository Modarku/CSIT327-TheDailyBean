# Generated by Django 5.1.2 on 2024-11-12 15:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_productid_review_product_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
