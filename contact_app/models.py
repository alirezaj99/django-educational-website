from django.db import models
from extensions.utils import jalali_converter

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11,verbose_name='شماره تماس',)
    subject = models.CharField(max_length=100,verbose_name='عنوان')
    message = models.TextField(verbose_name='متن پیام')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده / نشده')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارتباط")
    update_time = models.DateTimeField(auto_now=True,verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'تماس'
        verbose_name_plural = "تماس ها"
        ordering = ['-create_time']
    
    def __str__(self):
        return f'{self.subject} | {self.message[:40]}'

    def jalali_time(self):
        return jalali_converter(self.create_time)

    jalali_time.short_description = 'زمان ثبت'

    def get_message(self):
        if len(self.message) <= 100:
            return self.message[:100]
        else:
            return f'{self.message[:100]} ...'    
    
    get_message.short_description = 'پیام'