from django.urls import path
from .views import (
    Register, Login, logout_view, add_course_to_order, profile_update, Cart, delete_course_from_order, MyCourses,
    PasswordChange, CourseAdd, TeacherCourses, MyComment, TeacherBlogs, PaymentList, PaymentDetail, BlogCreate,VideoAdd
    , PasswordReset,PasswordResetConfirm
)

app_name = 'account'

urlpatterns = [
    path('cart/', Cart.as_view(), name='cart'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('password-change/', PasswordChange.as_view(), name='password_change'),
    path('profile/', profile_update, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('my-courses/', MyCourses.as_view(), name='my_courses'),
    path('add-courses-to-order/<int:pk>/', add_course_to_order, name='add_course_to_order'),
    path('delete-courses-from-order/<int:pk>/', delete_course_from_order, name='delete_course_to_order'),
    path('course-add/', CourseAdd.as_view(), name='course_add'),
    path('video-course-add/', VideoAdd.as_view(), name='video_course_add'),
    path('teacher-courses/', TeacherCourses.as_view(), name='teacher_courses'),
    path('my-comment/', MyComment.as_view(), name='my_comment'),
    path('teacher-blogs/', TeacherBlogs.as_view(), name='teacher_blogs'),
    path('blog-create/', BlogCreate.as_view(), name='blog_create'),
    path('payments/', PaymentList.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetail.as_view(), name='payment_detail'),
    path('password-reset/',PasswordReset.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
]
