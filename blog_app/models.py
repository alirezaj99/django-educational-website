from django.db import models
from account_app.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import random
import os
from extensions.utils import jalali_converter_year, jalali_converter_month, jalali_converter_day, jalali_converter,EmailService
from django.db.models.signals import pre_save,post_save
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html,strip_tags,html_safe

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
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='زمان ایجاد')
    update_time = models.DateTimeField(auto_now=True,verbose_name='زمان بروزرسانی')

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
    status = models.BooleanField(default=False, verbose_name="وضعیت انتشار")
    publish_time = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = BlogManager()

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-publish_time']

    def save(self):
        if self.pk:
            old = Blog.objects.get(pk=self.pk)
            if self.status == True and old.status == False:
                # sned email
                users = User.objects.filter(send_email = True)
                users_email = [user.email for user in users]
                current_site = '127.0.0.1:8000'
                blog_url = f"{current_site}{reverse('blog:blog_detail' ,kwargs={'pk':self.pk,'slug':self.slug})}"
                blog_title = self.title      
                blog_author = self.get_author_name()   
                if users_email:
                    subject = f'ایجوکمپ | مقاله جدیدی با عنوان {blog_title} انتشار یافت'
                    message = f'مقاله جدیدی با عنوان {blog_title} توسط {blog_author} انتشار یافت روی لینک زیر کلیلک کنید و آن را مطالعه کنید.'
                    EmailService.send_email(subject,users_email,'email/blog-create.html',{'head_title':subject,'message':message,'blog_url':blog_url,'blog_title':blog_title})
                # end send email
        super(Blog, self).save()



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

    get_jalali_date_for_url.short_description = 'تاریخ انتشار'

    def get_description(self):
         return strip_tags(self.description[:130])

    get_description.short_description = 'توضیحات'

    def count_of_hints(self):
        return self.hits.all().count()

    count_of_hints.short_description = 'تعداد بازدید'

    def show_image_in_admin(self):
        if self.image:
            return format_html(
                "<img width=100px height=75px  src='{}' >".format(self.image.url))
        else:
            return ''

    show_image_in_admin.short_description = 'تصویر' 

class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='blog_comments',
                             verbose_name='کاربر')
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True, related_name='comments',
                             verbose_name='دوره')
    message = models.TextField(verbose_name='نظر')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies',
                               verbose_name='پاسخ')
    active = models.BooleanField(default=False, verbose_name="تایید شده / نشده")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ثبت")
    updated = models.DateTimeField(auto_now=True, verbose_name="زمان ویرایش")

    objects = CommentManager()

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        ordering = ['-created']

    def save(self):
        if self.pk:
            old = Comment.objects.get(pk=self.pk)
            if self.active == True and old.active == False:
                # send email
                author_email = self.blog.author.email
                user_email = self.user.email
                if author_email == user_email :
                    author_email = False
                    user_email = False
                parent_email = False
                if self.parent :
                    parent_email = self.parent.user.email
                    if parent_email in [author_email,user_email]:
                        parent_email = False    
                current_site = '127.0.0.1:8000'
                blog_url = f"{current_site}{reverse('blog:blog_detail' ,kwargs={'pk':self.blog.pk,'slug':self.blog.slug})}"
                blog_title = self.blog.title        
                if author_email:
                    subject = f'برای مقاله شما {blog_title} دیدگاه جدیدی ثبت شد'
                    message = f'برای مقاله {blog_title} شما دیدگاه جدیدی توسط {self.user} ثبت شده است.\n'
                    EmailService.send_email(subject,[author_email],'email/blog-comment.html',{'head_title':subject,'message':message,'blog_url':blog_url,'blog_title':blog_title})
                if parent_email:
                    subject = f'کابر {self.user} به دیدگاه شما در مقاله {self.parent.blog.title} پاسخ داد'
                    message = f'کابر {self.user} به دیدگاه شما در مقاله {self.parent.blog.title} پاسخ داد'
                    EmailService.send_email(subject,[parent_email],'email/blog-comment.html',{'head_title':subject,'message':message,'blog_url':blog_url,'blog_title':blog_title})
                # end send email
        super(Comment, self).save()

    def __str__(self):
        return f'{str(self.blog)} | {str(self.user)} | {self.message[0:70]}'

    def get_user_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user

    get_user_name.short_description = 'نویسنده'

    def get_message(self):
        return self.message[:100]

    get_message.short_description = 'دیدگاه'
    
    def jalali_time(self):
        return jalali_converter(self.created)

    jalali_time.short_description = 'زمان ثبت'

    def get_parent_user(self):
        if self.parent:
            return self.parent.user.username
        return ''

    get_parent_user.short_description = 'پاسخ به کاربر'

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


def send_blog_email(sender, instance,created, *args, **kwargs):
    if created and instance.status == True:
        # sned email
        users = User.objects.filter(send_email = True)
        users_email = [user.email for user in users]
        current_site = '127.0.0.1:8000'
        blog_url = f"{current_site}{reverse('blog:blog_detail' ,kwargs={'pk':instance.pk,'slug':instance.slug})}"
        blog_title = instance.title      
        blog_author = instance.get_author_name()   
        if users_email:
            subject = f'ایجوکمپ | مقاله جدیدی با عنوان {blog_title} انتشار یافت'
            message = f'مقاله جدیدی با عنوان {blog_title} توسط {blog_author} انتشار یافت روی لینک زیر کلیلک کنید و آن را مطالعه کنید.'
            EmailService.send_email(subject,users_email,'email/blog-create.html',{'head_title':subject,'message':message,'blog_url':blog_url,'blog_title':blog_title})
        # end send email


pre_save.connect(set_blog_slug, Blog)
post_save.connect(send_blog_email, Blog)



