# Generated by Django 4.2.5 on 2024-03-08 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0019_alter_store_document_adhar_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store_details',
            name='abline1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='store_details',
            name='abline2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='store_details',
            name='city',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='store_details',
            name='district',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='store_details',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]