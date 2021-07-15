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


# model managers

class CourseManager(models.Manager):
    def get_publish_course(self):
        return self.get_queryset().filter(status='p')

    def get_course_by_category(self, category_slug):
        return self.get_queryset().filter(categories__slug__iexact=category_slug, status='p')


class CourseCategoryManager(models.Manager):
    def get_active_category(self):
        return self.get_queryset().filter(status=True)


# models
class CourseCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='عنوان در url')
    status = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    position = models.IntegerField(default=0, verbose_name='اولویت قرارگیری')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = CourseCategoryManager()

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['-position']

    def __str__(self):
        return self.title


class Course(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیشنویس'),
        ('p', 'منتشر شده'),
    )
    LEVEL_CHOICES = (
        ('b', 'مقدماتی'),
        ('m', 'متوسط'),
        ('a', 'پیشرفته'),
        ('bm', 'مقدماتی تا متوسط'),
        ('ma', 'متوسط تا پیشرفته'),
        ('ba', 'مقدماتی تا پیشرفته'),
    )
    title = models.CharField(max_length=200, verbose_name='عنوان دوره')
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    categories = models.ManyToManyField(CourseCategory, blank=True, related_name='course_category',
                                        verbose_name='دسته بندی')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='b', verbose_name='سطح دوره')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d', verbose_name='وضعیت')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = CourseManager()

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'
        ordering = ['-publish_time']

    def __str__(self):
        return self.title

    def course_url(self):
        return f"/courses/{self.pk}/{self.title}"

    def get_level(self):
        if self.level == 'b':
            return 'مقدماتی'
        elif self.level == 'm':
            return 'متوسط'
        elif self.level == 'a':
            return 'پیشرفته'
        elif self.level == 'bm':
            return 'مقدماتی تا متوسط'
        elif self.level == 'ma':
            return 'متوسط تا پیشرفته'
        elif self.level == 'ba':
            return 'مقدماتی تا پیشرفته'

    def category_to_str(self):
        return " - ".join([category.title for category in self.categories.get_active_category()])
