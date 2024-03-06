# Generated by Django 4.2.5 on 2024-03-06 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0016_store_document_bank_micr_store_document_cancel_check_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store_document',
            name='bank_micr',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='store_document',
            name='cancel_check',
            field=models.ImageField(null=True, upload_to='kyc/'),
        ),
        migrations.AddField(
            model_name='store_document',
            name='gst_certificate',
            field=models.ImageField(blank=True, null=True, upload_to='kyc/'),
        ),
        migrations.AlterField(
            model_name='store_document',
            name='gst_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='store_document',
            name='store_vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.store_details'),
        ),
        migrations.AlterField(
            model_name='store_document',
            name='trade_lisence',
            field=models.ImageField(blank=True, null=True, upload_to='kyc/'),
        ),
    ]
