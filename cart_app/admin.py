from django.contrib import admin
from .models import Cart,CartItem

# register models

admin.site.register(Cart)
admin.site.register(CartItem)