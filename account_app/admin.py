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

UserAdmin.list_display += ('is_teacher', 'is_student','send_email',)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
