# Generated by Django 5.1.1 on 2024-10-01 08:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', models.CharField(max_length=25, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin')], max_length=10)),
            ],
        ),
    ]
