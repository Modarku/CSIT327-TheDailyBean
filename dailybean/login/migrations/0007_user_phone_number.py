# Generated by Django 5.1.1 on 2024-11-27 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_alter_user_user_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]