from django.db import models
import os
import random


# generate image name
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 999)
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.site_title}-{random_num}{ext}"
    return f"settings/favicon/{final_name}"


# models
class Settings(models.Model):
    site_title = models.CharField(max_length=300, verbose_name='عنوان سایت')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    address = models.TextField(max_length=700,verbose_name='آدرس')
    phone_number = models.CharField(max_length=400,verbose_name='شماره تماس')
    instagram = models.CharField(max_length=300,blank=True, verbose_name='آی دی اینساگرام')
    twitter = models.CharField(max_length=300,blank=True, verbose_name='آی دی توییتر')
    youtube = models.URLField(blank=True, verbose_name='لینک یوتیوب')
    site_favicon = models.ImageField(upload_to=upload_image_path, verbose_name='آیکون هدر سایت')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "تنطیمات سایت"

    class Meta:
        verbose_name = 'تنظیم سایت'
        verbose_name_plural = 'تنظیمات سایت'
        ordering = ['-create_time']
