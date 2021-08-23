from django.urls import path
from .views import ContactCreate
app_name = 'contact'

urlpatterns = [
    path('',ContactCreate.as_view(),name='contact_create'),
]
