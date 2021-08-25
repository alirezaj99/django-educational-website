from django.shortcuts import render
from course_app.models import Course
from account_app.models import User

# Create your views here.

def about_us(request):
    courses_count = Course.objects.get_publish_course().count()
    teachers_count = User.objects.filter(is_teacher=True, is_active=True).count()
    students_count = User.objects.filter(is_student=True, is_active=True).count()
    context ={
        'courses_count' : courses_count ,
        'teachers_count' : teachers_count ,
        'students_count' : students_count ,
    }
    return render(request,'about-us/about-us.html',context)