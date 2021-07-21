from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.db.models.signals import post_save


# generate image name
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_avatar_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.user}{ext}"
    return f"user/profile/avatar/{final_name}"


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='آدرس ایمیل')
    is_teacher = models.BooleanField(default=False, verbose_name='وضعیت مدرسی')

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ['-is_superuser']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')
    phone_number = models.PositiveIntegerField(blank=True, null=True, unique=True, verbose_name='شماره تماس')
    web_site = models.URLField(blank=True, null=True, verbose_name='آدرس وب سایت')
    bio = models.TextField(max_length=700, blank=True, null=True, verbose_name='بیوگرافی')
    avatar = models.ImageField(upload_to=upload_avatar_path, blank=True, null=True, verbose_name='تصویر آواتار')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل ها'
        ordering = ['-create_time']

    def __str__(self):
        return f"{str(self.user)}"

    def get_avatar(self):
        try:
            return self.avatar.url
        except:
            return '/static/images/testimonials/pic2.jpg'


def create_profile(sender, **kwargs):
    if kwargs['created']:
        profile = Profile(user=kwargs['instance'])
        profile.save()


post_save.connect(create_profile, sender=User)
