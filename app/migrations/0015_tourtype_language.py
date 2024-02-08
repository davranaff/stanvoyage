# Generated by Django 5.0.1 on 2024-02-08 00:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_tourevent_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourtype',
            name='language',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, related_name='types', to='app.language'),
            preserve_default=False,
        ),
    ]