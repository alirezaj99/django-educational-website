from django.urls import path
from .views import Register, Login, logout_view, add_course_to_order

app_name = 'account'

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-courses-to-order/<int:pk>/', add_course_to_order, name='add_course_to_order'),
]
