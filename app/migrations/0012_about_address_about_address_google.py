# Generated by Django 5.0.1 on 2024-02-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_destination_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='about',
            name='address_google',
            field=models.URLField(null=True),
        ),
    ]