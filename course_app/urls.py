from django.urls import path
from .views import CourseList, CourseDetail

app_name = 'course'

urlpatterns = [
    path('courses/', CourseList.as_view(), name='course_list'),
    path('courses/<int:pk>/<slug>/', CourseDetail.as_view(), name='course_detail'),
]
