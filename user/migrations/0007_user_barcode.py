# Generated by Django 4.0.5 on 2022-09-20 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='barcode',
            field=models.ImageField(blank=True, upload_to='barcodes'),
        ),
    ]
