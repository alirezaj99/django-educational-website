from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
import os
import random
from account_app.models import User
from extensions.utils import jalali_converter
from django.db.models.signals import pre_save


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


def upload_video_path(instance, filename):
    random_num = random.randint(1, 999)
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.course.id}-{instance.position}-{instance.title}-{random_num}{ext}"
    return f"course/video/{final_name}"


# model managers

class CourseManager(models.Manager):
    def get_publish_course(self):
        return self.get_queryset().filter(status=True)

    def get_course_by_category(self, category_slug):
        return self.get_queryset().filter(categories__slug__iexact=category_slug, status=True)


class CourseCategoryManager(models.Manager):
    def get_active_category(self):
        return self.get_queryset().filter(status=True)


class VideoManager(models.Manager):
    def get_active_video(self):
        return self.get_queryset().filter(status=True)


class CommentManager(models.Manager):
    def get_active_comment(self):
        return self.get_queryset().filter(active=True, parent__isnull=True)

    def get_active_reply(self):
        return self.get_queryset().filter(active=True, parent__isnull=False)


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
    LEVEL_CHOICES = (
        ('b', 'مقدماتی'),
        ('m', 'متوسط'),
        ('a', 'پیشرفته'),
        ('bm', 'مقدماتی تا متوسط'),
        ('ma', 'متوسط تا پیشرفته'),
        ('ba', 'مقدماتی تا پیشرفته'),
    )
    LANGUAGE_CHOICES = (
        ('fa', 'فارسی'),
        ('en', 'انگلیسی'),
        ('mo', 'غیره'),
    )
    title = models.CharField(max_length=200, verbose_name='عنوان دوره')
    slug = models.CharField(max_length=200, verbose_name='عنوان در url', blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses', verbose_name='مدرس')
    image = models.ImageField(upload_to=upload_image_path, verbose_name='تصویر')
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    categories = models.ManyToManyField(CourseCategory, blank=True, related_name='course_category',
                                        verbose_name='دسته بندی')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='b', verbose_name='سطح دوره')
    language = models.CharField(max_length=2, default='fa', choices=LANGUAGE_CHOICES, verbose_name='زبان دوره')
    is_finish = models.BooleanField(default=False, verbose_name='آیا دوره تمام شده؟')
    status = models.BooleanField(default=False, verbose_name='آیا نمایش داده شود؟')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = CourseManager()

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره ها'
        ordering = ['-publish_time']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title.replace(' ', '-'))
        return super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def course_url(self):
        return f"/courses/{self.pk}/{self.title.replace(' ', '-')}"

    def total_time(self):
        total = 0
        for video in self.video.get_active_video():
            secs = video.time.hour * 3600 + video.time.minute * 60 + video.time.second
            total += secs

        # return datetime.time(total // 3600, (total % 3600) // 60, total % 60)
        def hour_return():
            if len(str(total // 3600)) == 1:
                return f"0{total // 3600}"
            else:
                return total // 3600

        def minute_return():
            if len(str((total % 3600) // 60)) == 1:
                return f"0{(total % 3600) // 60}"
            else:
                return (total % 3600) // 60

        def second_return():
            if len(str(total % 60)) == 1:
                return f"0{total % 60}"
            else:
                return total % 60

        return f"{hour_return()}:{minute_return()}:{second_return()}"

    def jalali_time(self):
        return jalali_converter(self.publish_time)

    jalali_time.short_description = 'زمان انتشار'

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

    def get_language(self):
        if self.language == 'fa':
            return 'فارسی'
        elif self.language == 'en':
            return 'انگلیسی'
        elif self.language == 'mo':
            return 'غیره'

    def finish(self):
        if self.is_finish:
            return 'به پایان رسیده'
        else:
            return 'در حال برگزاری'

    def get_teacher_name(self):
        if self.teacher.get_full_name():
            return self.teacher.get_full_name()
        else:
            return self.teacher

    def category_to_str(self):
        return " - ".join([category.title for category in self.categories.get_active_category()])


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان جلسه")
    video = models.FileField(upload_to=upload_video_path, verbose_name='ویدیو')
    position = models.PositiveIntegerField(default=0, unique=True, verbose_name='شماره جلسه')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='video',
                               verbose_name='دوره')
    description = models.TextField(verbose_name="توضیحات")
    time = models.TimeField(verbose_name='زمان ویدیو')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")

    objects = VideoManager()

    class Meta:
        verbose_name = 'ویدیو'
        verbose_name_plural = 'ویدیوها'
        ordering = ['position']

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='comments',
                             verbose_name='کاربر')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='comments',
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
        return f'{str(self.course)} | {str(self.user)} | {self.message[0:70]}'

    def get_user_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user

    def jalali_time(self):
        return jalali_converter(self.created)

    jalali_time.short_description = 'زمان ثبت'


def set_course_slug(sender, instance, *args, **kwargs):
    instance.slug = instance.title.replace(' ', '-')


pre_save.connect(set_course_slug, Course)
