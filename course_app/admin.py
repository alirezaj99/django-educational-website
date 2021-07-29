from django.contrib import admin
from .models import Course, CourseCategory, Video, Comment, CourseTag


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


class CourseTagAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'position']
    list_editable = ['position', 'status']

    class meta:
        model = CourseTag


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(CourseTag, CourseTagAdmin)
admin.site.register(Video)
admin.site.register(Comment)
