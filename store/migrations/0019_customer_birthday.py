# Generated by Django 4.2.5 on 2024-02-22 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_remove_order_invoices_customer_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
    ]
