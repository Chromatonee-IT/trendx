# Generated by Django 4.2.5 on 2024-02-28 07:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0027_customer_referred_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='referred_by',
        ),
        migrations.AddField(
            model_name='customer',
            name='referred_by_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referred_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
