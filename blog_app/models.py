from django.db import models
from account_app.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import random
import os
from extensions.utils import jalali_converter_year, jalali_converter_month, jalali_converter_day, jalali_converter
from django.db.models.signals import pre_save
from django.db.models import Q


# generate image name
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 999)
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.get_jalali_date_for_url()}/{instance.title.replace(' ', '-')}-{random_num}{ext}"
    return f"blog/img/{final_name}"


# model managers
class BlogManager(models.Manager):
    def get_publish_blog(self):
        return self.get_queryset().filter(status=True)

    def search(self, query):
        lookup = (
                Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, status=True).distinct()


class BlogTagManager(models.Manager):
    def get_active_tag(self):
        return self.get_queryset().filter(status=True)


class CommentManager(models.Manager):
    def get_active_comment(self):
        return self.get_queryset().filter(active=True, parent__isnull=True)

    def get_active_reply(self):
        return self.get_queryset().filter(active=True, parent__isnull=False)


# models

class BlogTag(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان برچسب')
    status = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = BlogTagManager()

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'
        ordering = ['-create_time']

    def __str__(self):
        return self.title


class Blog(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='blogs',
                               verbose_name="نویسنده")
    title = models.CharField(max_length=300, verbose_name="عنوان مقاله")
    slug = models.CharField(max_length=300, verbose_name='عنوان در url', blank=True)
    description = RichTextUploadingField(verbose_name="محتوا")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="تصویر مقاله")
    tags = models.ManyToManyField(BlogTag, related_name='blogs', blank=True, verbose_name='تگ ها / برچسب ها')
    hits = models.ManyToManyField('IpAddress', blank=True, related_name="articles", verbose_name="بازید")
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    send_email = models.BooleanField(default=True, verbose_name='ارسال ایمیل')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = BlogManager()

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-publish_time']

    def __str__(self):
        return self.title

    def get_author_name(self):
        if self.author.get_full_name():
            return self.author.get_full_name()
        else:
            return self.author

    get_author_name.short_description = 'نویسنده'

    def get_jalali_date_for_url(self):
        return f'{jalali_converter_year(self.publish_time)}/{jalali_converter_month(self.publish_time)}/{jalali_converter_day(self.publish_time)}'


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='blog_comments',
                             verbose_name='کاربر')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, related_name='comments',
                             verbose_name='دوره')
    message = models.TextField(verbose_name='نظر')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies',
                               verbose_name='پاسخ')
    active = models.BooleanField(default=True, verbose_name="فعال / غیرفعال")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    updated = models.DateTimeField(auto_now=True, verbose_name="زمان ویرایش")

    objects = CommentManager()

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created']

    def __str__(self):
        return f'{str(self.blog)} | {str(self.user)} | {self.message[0:70]}'

    def get_user_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user

    def jalali_time(self):
        return jalali_converter(self.created)

    jalali_time.short_description = 'زمان ثبت'


class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="آی پی آدرس")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")

    class Meta:
        verbose_name = "آی پی آدرس"
        verbose_name_plural = "آی پی آدرس ها"

    def __str__(self):
        return self.ip_address

    def jtime(self):
        return jalali_converter(self.create_time)

    jtime.short_description = "زمان ثبت"


def set_blog_slug(sender, instance, *args, **kwargs):
    instance.slug = instance.title.replace(' ', '-')


pre_save.connect(set_blog_slug, Blog)
