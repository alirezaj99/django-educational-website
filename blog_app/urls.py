from django.urls import path
from .views import BlogList, BlogDetail

app_name = 'blog'

urlpatterns = [
    path('blogs/', BlogList.as_view(), name='blog_list'),
    path('blogs/<int:pk>/<slug>/', BlogDetail.as_view(), name='blog_detail'),
]
