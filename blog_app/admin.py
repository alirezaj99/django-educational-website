from django.contrib import admin
from .models import Blog, BlogTag

# Register your models here.

admin.site.register(Blog)
admin.site.register(BlogTag)
