# Generated by Django 3.2.5 on 2022-02-19 12:03

import ckeditor.fields
import course_app.models
from django.conf import settings
import django.core.validators
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
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان دوره')),
                ('slug', models.CharField(blank=True, max_length=200, verbose_name='عنوان در url')),
                ('image', models.ImageField(upload_to=course_app.models.upload_image_path, verbose_name='تصویر')),
                ('description', ckeditor.fields.RichTextField(verbose_name='توضیحات')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('discount', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('level', models.CharField(choices=[('b', 'مقدماتی'), ('m', 'متوسط'), ('a', 'پیشرفته'), ('bm', 'مقدماتی تا متوسط'), ('ma', 'متوسط تا پیشرفته'), ('ba', 'مقدماتی تا پیشرفته')], default='b', max_length=2, verbose_name='سطح دوره')),
                ('language', models.CharField(choices=[('fa', 'فارسی'), ('en', 'انگلیسی'), ('mo', 'غیره')], default='fa', max_length=2, verbose_name='زبان دوره')),
                ('is_finish', models.BooleanField(default=False, verbose_name='آیا دوره تمام شده؟')),
                ('status', models.BooleanField(default=False, verbose_name='آیا نمایش داده شود؟')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'دوره',
                'verbose_name_plural': 'دوره ها',
                'ordering': ['-publish_time'],
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='عنوان دسته بندی')),
                ('position', models.IntegerField(default=0, verbose_name='اولویت قرارگیری')),
                ('status', models.BooleanField(default=True, verbose_name='فعال/غیرفعال')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['position', '-create_time'],
            },
        ),
        migrations.CreateModel(
            name='CourseTag',
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
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان جلسه')),
                ('video', models.FileField(upload_to=course_app.models.upload_video_path, verbose_name='ویدیو')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='شماره جلسه')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('time', models.TimeField(verbose_name='زمان ویدیو')),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان انتشار')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='video', to='course_app.course', verbose_name='دوره')),
            ],
            options={
                'verbose_name': 'ویدیو',
                'verbose_name_plural': 'ویدیوها',
                'ordering': ['position'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='course_category', to='course_app.CourseCategory', verbose_name='دسته بندی'),
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(blank=True, related_name='student_courses', to=settings.AUTH_USER_MODEL, verbose_name='دانشجو'),
        ),
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='course_tag', to='course_app.CourseTag', verbose_name='برچسب'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_courses', to=settings.AUTH_USER_MODEL, verbose_name='مدرس'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='نظر')),
                ('active', models.BooleanField(default=False, verbose_name='تایید شده / نشده ؟')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='course_app.course', verbose_name='دوره')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replies', to='course_app.comment', verbose_name='پاسخ')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
                'ordering': ['-created'],
            },
        ),
    ]
