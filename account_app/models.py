from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.db.models.signals import post_save
import random
from django.core.validators import RegexValidator
from extensions.utils import jalali_converter
from django.utils.html import format_html

# generate image name

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_avatar_path(instance, filename):
    random_num = random.randint(1, 999)
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.user}-{random_num}{ext}"
    return f"user/profile/avatar/{final_name}"


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
    is_teacher = models.BooleanField(default=False, verbose_name='وضعیت مدرسی')
    is_student = models.BooleanField(default=False, verbose_name='وضعیت دانشجویی')
    send_email = models.BooleanField(default=True, verbose_name='ارسال ایمیل')

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ['-is_superuser', '-is_teacher']

    def fullname_or_username(self):
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.username    


class Profile(models.Model):
    # validator
    phone_number_validator = RegexValidator(regex=r'^[0][9]\d{9}$',message='شماره موبایل نامعتبر است.',flags=0,)
    #end validator
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')
    phone_number = models.CharField(max_length=11,unique=True,verbose_name='شماره موبایل',validators=[phone_number_validator],blank=True,null=True)
    web_site = models.URLField(blank=True, null=True, verbose_name='آدرس وب سایت')
    bio = models.TextField(max_length=700, blank=True, null=True, verbose_name='بیوگرافی')
    avatar = models.ImageField(upload_to=upload_avatar_path, blank=True, null=True, verbose_name='تصویر آواتار')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='زمان ایجاد')
    update_time = models.DateTimeField(auto_now=True,verbose_name='زمان بروزرسانی')

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
        ordering = ['-create_time']

    def __str__(self):
        return f"{str(self.user)}"

    def jalali_time(self):
        return jalali_converter(self.create_time)

    jalali_time.short_description = 'زمان ایجاد'
    
    def jalali_update_time(self):
        return jalali_converter(self.update_time)

    jalali_update_time.short_description = 'آخرین بروزرسانی'

    def get_bio(self):
        if self.bio:
            if len(self.bio) <= 100:
                return self.bio[:100]
            else:
                return f'{self.bio[:100]} ...'    
        else:
            return ''
    get_bio.short_description = 'پیام'

    def get_avatar(self):
        try:
            return self.avatar.url
        except:
            return '/static/images/testimonials/pic2.jpg'
    
    def show_avatar_in_admin(self):
        return format_html(
            "<img style='border-radius: 50px' width=55px height=55px  src='{}' >".format(self.get_avatar()))

    show_avatar_in_admin.short_description = 'آواتار'

def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile(user=kwargs['instance'])
        profile.save()


post_save.connect(create_profile, sender=User)
