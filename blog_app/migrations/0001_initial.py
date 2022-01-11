# Generated by Django 3.2.5 on 2022-01-11 21:03

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
                ('status', models.BooleanField(default=False, verbose_name='وضعیت انتشار')),
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
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='عنوان برچسب')),
                ('status', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
            ],
            options={
                'verbose_name': 'برچسب',
                'verbose_name_plural': 'برچسب ها',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آی پی آدرس')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')),
            ],
            options={
                'verbose_name': 'آی پی آدرس',
                'verbose_name_plural': 'آی پی آدرس ها',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='نظر')),
                ('active', models.BooleanField(default=False, verbose_name='تایید شده / نشده')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('blog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='blog_app.blog', verbose_name='دوره')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='blog_app.comment', verbose_name='پاسخ')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
                'ordering': ['-created'],
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='articles', to='blog_app.IpAddress', verbose_name='بازید'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='blogs', to='blog_app.BlogTag', verbose_name='تگ ها / برچسب ها'),
        ),
    ]
