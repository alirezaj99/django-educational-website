from django.shortcuts import render
from course_app.models import Course,CourseCategory
from account_app.models import User
from blog_app.models import Blog
from settings_app.models import Settings

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

# render partial

def header_references(request):
    try:
        settings = Settings.objects.first()
        icon = settings.site_favicon.url
    except:
        icon = ""
    context = {
        'icon': icon,
    }
    return render(request, 'Shared/_HeaderReferences.html', context)


def site_header(request):
    categories = CourseCategory.objects.get_active_category()
    
    try:
        settings = Settings.objects.first()
        email = settings.email
        instagram = settings.instagram
        youtube = settings.youtube
        twitter = settings.twitter
    except:
        email = ""
        instagram = ""
        youtube = ""
        twitter = ""

    context = {
        'categories': categories,
        'email': email,
        'instagram': instagram,
        'youtube': youtube,
        'twitter': twitter,
    }
    return render(request, 'Shared/Header.html', context)


def footer(request):
    categories = CourseCategory.objects.get_active_category()[:4]
    blogs = Blog.objects.get_publish_blog()[:8]

    try:
        settings = Settings.objects.first()
        instagram = settings.instagram
        youtube = settings.youtube
        twitter = settings.twitter
        site_title = settings.site_title
    except:
        instagram = ""
        youtube = ""
        twitter = ""
        site_title = ""

    context = {
        'categories': categories,
        'blogs': blogs,
        'instagram': instagram,
        'youtube': youtube,
        'twitter': twitter,
        'site_title': site_title,
    }
    return render(request, 'Shared/Footer.html', context)
