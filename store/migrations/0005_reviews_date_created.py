# Generated by Django 4.2.5 on 2023-11-25 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_reviews_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]