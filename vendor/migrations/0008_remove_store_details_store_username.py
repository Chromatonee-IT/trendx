# Generated by Django 4.2.5 on 2024-02-25 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_remove_store_details_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store_details',
            name='store_username',
        ),
    ]
