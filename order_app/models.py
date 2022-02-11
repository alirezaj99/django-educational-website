from django.db import models
from django.conf import settings
from course_app.models import Course
from django.db.models.signals import post_save, pre_save
from extensions.utils import jalali_converter,jalali_converter_date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.

class Order(models.Model):
    
    STATUS_CHOICES = [
        ('w','waiting'), # در انتظار پدراخت
        ('s','success'), # پرداخت موفق
        ('f','failed'), # پرداخت ناموفق
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders',
                             verbose_name='کاربر')
    coupon_code = models.ForeignKey("CouponCode",on_delete=models.SET_NULL,related_name='orders',blank=True,null=True,verbose_name='کد تخفیف')
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='w')
    is_free = models.BooleanField(default=False, verbose_name='رایگان؟')
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ پرداخت")
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ['-payment_date', '-created']

    def __str__(self):
        return f'{str(self.user)}'

    def get_total_price(self):
        amount = 0
        for item in self.items.all():
            amount += item.total_price()
        if self.coupon_code:    
            total = amount - (amount * self.coupon_code.discount) / 100    
            return int(total)
        return amount

    get_total_price.short_description = 'جمع سفارش قابل پرداخت'

    def get_total_discount(self):
        amount = 0
        for item in self.items.all():
            amount += item.total_discount()
        return amount

    get_total_discount.short_description = 'جمع تخفیف'

    def get_price(self):
        amount = 0
        for item in self.items.all():
            amount += item.price
        return amount

    get_price.short_description = 'جمع سفارش اولیه'

    def jalali_time(self):
        return jalali_converter(self.created)
    
    jalali_time.short_description = 'زمان ایجاد'

    def jalali_payment_time(self):
        return jalali_converter(self.payment_date)
    
    jalali_payment_time.short_description = 'زمان پرداخت'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='order_items', verbose_name='دوره')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    discount = models.PositiveIntegerField(blank=True, null=True,
                                           validators=[MinValueValidator(1), MaxValueValidator(100)],
                                           verbose_name='درصد تخفیف')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')

    def total_price(self):
        if self.discount:
            total = (self.price * self.discount) / 100
            return int(self.price - total)
        else:
            return self.price

    def total_discount(self):
        if self.discount:
            total = (self.price * self.discount) / 100
            return int(total)
        else:
            return 0

    def __str__(self):
        return f'{str(self.course)} | {str(self.order)}'

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'
        ordering = ['-created']


class CouponCode(models.Model):
    code = models.CharField(max_length=50,verbose_name='کد تخفیف',unique=True)
    discount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],verbose_name='درصد تخفیف')
    start = models.DateTimeField(default=timezone.now,verbose_name='زمان شروع')
    end = models.DateTimeField(verbose_name='زمان پایان')
    status = models.BooleanField(default=True,verbose_name='فعال / غیرفعال؟')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')
    
    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'
        ordering = ['-status', '-created']

    def __str__(self):
        return f'{self.code} | {self.discount} %'
    
    def jalali_start(self):
        return jalali_converter_date(self.start)
    
    jalali_start.short_description = 'تاریخ شروع'
    
    def jalali_end(self):
        return jalali_converter_date(self.end)
    
    jalali_end.short_description = 'تاریخ پایان'
    

# def set_order_item_price(sender, instance, *args, **kwargs):
#     orders = Order.objects.filter(is_paid=False)
#     for order in orders:
#         items = order.items.filter(course_id=instance.id)
#         if items:
#             for item in items:
#                 item.price = instance.price
#                 item.discount = instance.discount
#                 item.save()


# pre_save.connect(set_order_item_price, Course)


