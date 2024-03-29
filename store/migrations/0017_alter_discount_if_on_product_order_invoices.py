# Generated by Django 4.2.5 on 2024-02-22 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_store_details_store_images_and_more'),
        ('store', '0016_rename_is_created_discount_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='if_on_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.products'),
        ),
        migrations.CreateModel(
            name='order_invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_amount', models.IntegerField(blank=True, max_length=50, null=True)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('if_updated', models.DateTimeField(auto_now=True)),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.orders')),
                ('vendor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.store_details')),
            ],
        ),
    ]
