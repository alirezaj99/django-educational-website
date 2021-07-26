from django.contrib import admin
from .models import Course, CourseCategory, Video, Comment


# Register your models here.

class VideoCourseInlines(admin.TabularInline):
    model = Video
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [VideoCourseInlines]

    class meta:
        model = Course


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'position']
    list_editable = ['position', 'status']

    class meta:
        model = CourseCategory


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Video)
admin.site.register(Comment)
