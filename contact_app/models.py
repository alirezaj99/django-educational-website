from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone_number = models.PositiveIntegerField(verbose_name='شماره تماس')
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