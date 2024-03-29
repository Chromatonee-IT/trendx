# Generated by Django 4.2.5 on 2024-02-24 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_store_details_store_images_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store_details',
            name='abline1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store_details',
            name='abline2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store_details',
            name='abline3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store_details',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store_details',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store_details',
            name='district',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store_details',
            name='state',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='store_details',
            name='zip',
            field=models.IntegerField(default=0),
        ),
    ]
