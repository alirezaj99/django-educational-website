from django.db import models
from account_app.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import random
import os
from extensions.utils import jalali_converter_year, jalali_converter_month, jalali_converter_day
from django.db.models.signals import pre_save


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


class Blog(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='blogs',
                               verbose_name="نویسنده")
    title = models.CharField(max_length=300, verbose_name="عنوان مقاله")
    slug = models.CharField(max_length=300, verbose_name='عنوان در url', blank=True)
    description = RichTextUploadingField(verbose_name="محتوا")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="تصویر مقاله")
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    send_email = models.BooleanField(default=True, verbose_name='ارسال ایمیل')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-publish_time']

    def __str__(self):
        return self.title

    def author_str(self):
        return str(self.author)

    author_str.short_description = 'نویسنده'

    def get_jalali_date_for_url(self):
        return f'{jalali_converter_year(self.publish_time)}/{jalali_converter_month(self.publish_time)}/{jalali_converter_day(self.publish_time)}'


def set_blog_slug(sender, instance, *args, **kwargs):
    instance.slug = instance.title.replace(' ', '-')


pre_save.connect(set_blog_slug, Blog)