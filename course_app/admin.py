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
    
    list_display = ['title','get_teacher_name','show_image_in_admin','price','discount','total_price','category_to_str','total_time','is_finish','count_of_student','jalali_time','status']
    list_filter = ['status','is_finish']
    search_fields = ['title','categories__title','tags__title','teacher__username','teacher__first_name','teacher__last_name']
    inlines = [VideoCourseInlines]

    class meta:
        model = Course


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'position']
    list_editable = ['position', 'status']
    list_filter = ['status','create_time']
    search_fields = ['title']

    class meta:
        model = CourseCategory


class CourseTagAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_editable = ['status']
    list_filter = ['status','create_time']
    search_fields = ['title']

    class meta:
        model = CourseTag

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title','position','video','course','time','publish_time','status']
    list_filter = ['status','publish_time']
    search_fields = ['title','course__title']

    class meta:
        model = Video

class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_user_name','course','get_message','get_parent_user','jalali_time','active']
    list_filter = ['active','created']
    search_fields = ['user__username','user__first_name','user__last_name','parent__message','parent__user__username','parent__user__first_name','parent__user__last_name','message']

    class meta:
        model = Comment

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(CourseTag, CourseTagAdmin)
admin.site.register(Video,VideoAdmin)
admin.site.register(Comment,CommentAdmin)
