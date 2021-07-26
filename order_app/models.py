from django.db import models
from django.conf import settings
from course_app.models import Course


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders',
                             verbose_name='کاربر')
    is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده/نشده؟')
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ پرداخت")
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ['-created']

    def __str__(self):
        return f'{str(self.user)}'

    def get_total_price(self):
        amount = 0
        for item in self.items.all():
            amount += item.price
        return amount

    get_total_price.short_description = 'جمع سفارش'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items', verbose_name='دوره')
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')

    def __str__(self):
        return f'{str(self.course)} | {str(self.order)}'

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'
        ordering = ['-created']
