from django.urls import path
from .views import Register, Login, logout_view, add_course_to_order, profile_update, Cart, delete_course_from_order

app_name = 'account'

urlpatterns = [
    path('cart/', Cart.as_view(), name='cart'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', profile_update, name='profile'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-courses-to-order/<int:pk>/', add_course_to_order, name='add_course_to_order'),
    path('delete-courses-from-order/<int:pk>/', delete_course_from_order, name='delete_course_to_order'),
]
