# Generated by Django 3.2.5 on 2022-01-11 21:03

from django.db import migrations, models
import settings_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(max_length=300, verbose_name='عنوان سایت')),
                ('email', models.EmailField(max_length=100, verbose_name='ایمیل')),
                ('address', models.TextField(max_length=700, verbose_name='آدرس')),
                ('phone_number', models.CharField(max_length=400, verbose_name='شماره تماس')),
                ('instagram', models.CharField(blank=True, max_length=300, verbose_name='آی دی اینساگرام')),
                ('twitter', models.CharField(blank=True, max_length=300, verbose_name='آی دی توییتر')),
                ('youtube', models.URLField(blank=True, verbose_name='لینک یوتیوب')),
                ('site_favicon', models.ImageField(upload_to=settings_app.models.upload_image_path, verbose_name='آیکون هدر سایت')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'تنظیم سایت',
                'verbose_name_plural': 'تنظیمات سایت',
                'ordering': ['-create_time'],
            },
        ),
    ]
