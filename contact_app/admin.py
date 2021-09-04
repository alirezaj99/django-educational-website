from django.contrib import admin
from .models import Contact

# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone_number','subject','get_message','jalali_time','is_read']
    list_filter = ['is_read','create_time']
    search_fields = ['name','subject','message','phone_number','email']

    class meta:
        model = Contact

admin.site.register(Contact,ContactAdmin)