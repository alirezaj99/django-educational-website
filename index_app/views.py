from django.shortcuts import render
from course_app.models import Course


# Create your views here.

def index_page(request):
    last_courses = Course.objects.get_publish_course()[:8]
    popular_courses = Course.objects.get_popular_course()
    courses_count = Course.objects.get_publish_course().count()
    context = {
        'last_courses': last_courses,
        'popular_courses': popular_courses,
        'courses_count': courses_count,
    }

    return render(request, 'index/index.html', context)
