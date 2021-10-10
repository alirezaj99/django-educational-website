from django.shortcuts import render
from course_app.models import Course
from account_app.models import User
from blog_app.models import Blog


# Create your views here.

def index_page(request):
    last_courses = Course.objects.get_publish_course()[:8]
    popular_courses = Course.objects.get_popular_course()[:8]
    courses_count = Course.objects.get_publish_course().count()
    teachers_count = User.objects.filter(is_teacher=True, is_active=True).count()
    students_count = User.objects.filter(is_student=True, is_active=True).count()
    last_blogs = Blog.objects.get_publish_blog()[:6]
    context = {
        'last_courses': last_courses,
        'popular_courses': popular_courses,
        'courses_count': courses_count,
        'teachers_count': teachers_count,
        'students_count': students_count,
        'last_blogs': last_blogs,
    }

    return render(request, 'index/index.html', context)
