from django.urls import path
from .views import go_to_gateway_view, callback_gateway_view

app_name = 'order'

urlpatterns = [
    path('payment/request/', go_to_gateway_view, name='request'),
    path('payment/call-back/', callback_gateway_view, name='call_back'),
]
