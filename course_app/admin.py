from django.contrib import admin
from .models import Course, CourseCategory, Video, Comment, CourseTag
from account_app.models import User

# Register your models here.

class VideoCourseInlines(admin.TabularInline):
    model = Video
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(is_teacher=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
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
