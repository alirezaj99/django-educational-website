from django.contrib import admin
from .models import Blog, BlogTag, Comment

# Register your models here.

admin.site.register(Blog)
admin.site.register(BlogTag)
admin.site.register(Comment)
