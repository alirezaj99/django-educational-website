from django.contrib import admin
from .models import Cart,CartItem

# register models

class CartItemInlines(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','coupon_code','count_of_items']
    list_filter = ['created','update']
    search_fields = ['user__username','user__email','user__first_name','user__last_name']

    inlines = [CartItemInlines]

    class meta:
        model = Cart


admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem)