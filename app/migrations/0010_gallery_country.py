# Generated by Django 5.0.1 on 2024-02-06 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_rename_is_new_blog_is_popular'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='galleries', to='app.country'),
            preserve_default=False,
        ),
    ]
