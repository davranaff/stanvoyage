# Generated by Django 5.0.1 on 2024-02-05 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_about_created_at_blogtag_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='preview_image',
            field=models.ImageField(null=True, upload_to='tours/preview_images/'),
        ),
    ]
