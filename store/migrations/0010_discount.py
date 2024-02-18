# Generated by Django 4.2.5 on 2024-02-15 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_orders_delete_orders_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer', models.CharField(max_length=20, null=True)),
                ('offer_cat', models.CharField(max_length=3)),
                ('discount_value', models.CharField(blank=True, max_length=6, null=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('if_on_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.category')),
            ],
        ),
    ]
