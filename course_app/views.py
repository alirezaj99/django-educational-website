from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from course_app.models import Course


# Create your views here.

class CourseList(ListView):
    queryset = Course.objects.all()
    template_name = 'course/course-list.html'
    paginate_by = 9


class CourseDetail(DetailView):
    def get_object(self):
        course = get_object_or_404(Course.objects.all(), pk=self.kwargs.get('pk'), title=self.kwargs.get('slug'))
        return course

    template_name = 'course/course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
