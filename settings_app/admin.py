from django.contrib import admin
from .models import Settings

# Register your models here.

class SettingsAdmin(admin.ModelAdmin):
    list_display = ['site_title','email','address','phone_number','instagram','twitter','youtube','show_favicon_in_admin','jalali_time','jalali_update_time']

    class meta:
        model = Settings

admin.site.register(Settings,SettingsAdmin)
