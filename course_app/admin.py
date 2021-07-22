from django.contrib import admin
from .models import Course, CourseCategory, Video, Comment


# Register your models here.

class VideoCourseInlines(admin.TabularInline):
    model = Video
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [VideoCourseInlines]

    class meta:
        model = Course


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory)
admin.site.register(Video)
admin.site.register(Comment)
