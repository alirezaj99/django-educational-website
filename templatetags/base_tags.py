from django import template
from django.template.loader import get_template
from settings_app.models import Settings
	
register = template.Library()

@register.simple_tag
def site_title():

    try:
        settings = Settings.objects.first()
        site_title = settings.site_title
    except:
        site_title = 'عنوان سایت'

    return site_title