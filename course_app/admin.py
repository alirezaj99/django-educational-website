from django.contrib import admin
from .models import Course, CourseCategory, Video

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(Video)
