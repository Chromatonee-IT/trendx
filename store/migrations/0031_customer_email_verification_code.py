# Generated by Django 4.2.5 on 2024-02-29 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_lastlogin_browser_name_lastlogin_device_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email_verification_code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
