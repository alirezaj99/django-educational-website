# Generated by Django 3.2.5 on 2021-07-21 11:15

import account_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0003_alter_profile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=account_app.models.upload_avatar_path, verbose_name='تصویر آواتار'),
        ),
    ]