# Generated by Django 3.2.5 on 2021-08-07 22:48

import blog_app.models
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان مقاله')),
                ('slug', models.CharField(blank=True, max_length=300, verbose_name='عنوان در url')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='محتوا')),
                ('image', models.ImageField(upload_to=blog_app.models.upload_image_path, verbose_name='تصویر مقاله')),
                ('status', models.BooleanField(default=False, verbose_name='وضعیت')),
                ('send_email', models.BooleanField(default=True, verbose_name='ارسال ایمیل')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blogs', to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
                'ordering': ['-publish_time'],
            },
        ),
    ]
