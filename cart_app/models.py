from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from course_app.models import Course
from django.core.validators import MinValueValidator,MaxValueValidator
# models 
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart',
                             verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'
        ordering = ['-update']

    def get_total_price(self):
        amount = 0
        for item in self.items.all():
            amount += item.total_price()
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


    def __str__(self):
        return f'{str(self.user)}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='سبد خرید')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_items', verbose_name='دوره')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    discount = models.PositiveIntegerField(blank=True, null=True,validators=[MinValueValidator(1), MaxValueValidator(100)],verbose_name='درصد تخفیف')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی')

    class Meta:
    	verbose_name = 'ایتم سبد خرید'
    	verbose_name_plural = 'ایتم سبد خرید'
    	ordering = ['-update']

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
        return f'{str(self.cart)}'

# signals
def create_cart(sender,created,instance,**kwargs):
    if created:
        cart = Cart(user=instance)
        cart.save()

post_save.connect(create_cart, sender=settings.AUTH_USER_MODEL)
