from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.

class OrderItemInlines(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_paid', 'get_total_price', 'payment_date']
    inlines = [OrderItemInlines]

    class meta:
        model = Order


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'discount']
    list_editable = ['discount']

    class meta:
        model = OrderItem


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
