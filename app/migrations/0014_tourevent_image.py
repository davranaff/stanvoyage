# Generated by Django 5.0.1 on 2024-02-07 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_country_description_country_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourevent',
            name='image',
            field=models.ImageField(null=True, upload_to='tours/event_images/'),
        ),
    ]