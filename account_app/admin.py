from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'is_teacher',
    'is_student',
    'send_email',
    'groups',
    'user_permissions',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone_number','web_site','get_bio','show_avatar_in_admin','jalali_time','jalali_update_time']
    list_filter = ['create_time']
    search_fields = ['user__username','user__email','user__first_name','user__last_name','bio','phone_number','web_site']

    class meta:
        model = Profile

UserAdmin.list_display += ('is_active','is_teacher', 'is_student','send_email',)
UserAdmin.list_filter += ('is_teacher', 'is_student','send_email',)
admin.site.register(User, UserAdmin)
admin.site.register(Profile,ProfileAdmin)
