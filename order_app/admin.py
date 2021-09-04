from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.

class OrderItemInlines(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','get_price','get_total_discount','get_total_price', 'is_paid','is_free', 'jalali_payment_time']
    list_filter = ['is_paid','is_free','payment_date']
    search_fields = ['user__username','user__email','user__first_name','user__last_name']

    inlines = [OrderItemInlines]

    class meta:
        model = Order


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'course', 'price','discount']
    list_filter = ['created']
    search_fields = ['order__user__username','order__user__email','order__user__first_name','order__user__last_name','course__title','course__description','course__tags__title','price','discount']

    class meta:
        model = OrderItem


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
