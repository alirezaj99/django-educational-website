from django.db import models
from django.utils import timezone
import os
import random


# generate image name
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 989999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{random_num}-{instance.title}{ext}"
    return f"course/cover-image/{final_name}"


# models
class Course(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیشنویس'),
        ('p', 'منتشر شده'),
    )
    LEVEL_CHOICES = (
        ('b', 'مبتدی'),
        ('m', 'متوسط'),
        ('a', 'پیشرفته'),
        ('bm', 'مبتدی تا متوسط'),
        ('ma', 'متوسط تا پیشرفته'),
        ('ba', 'مبتدی تا پیشرفته'),
    )
    title = models.CharField(max_length=200, verbose_name='عنوان دوره')
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='b', verbose_name='سطح دوره')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d', verbose_name='وضعیت')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'
        ordering = ['-publish_time']

    def __str__(self):
        return self.title
