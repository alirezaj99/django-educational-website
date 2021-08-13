from django.urls import path
from .views import send_request, verify

app_name = 'order'

urlpatterns = [
    path('payment/request/', send_request, name='send_request'),
    path('payment/verify/', verify, name='verify'),
]
