from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from course_app.models import Course, CourseCategory
from django.http import Http404


# Create your views here.

class CourseList(ListView):
    queryset = Course.objects.get_publish_course()
    template_name = 'course/course-list.html'
    paginate_by = 9


class CourseDetail(DetailView):
    def get_object(self):
        course = get_object_or_404(Course.objects.get_publish_course(), pk=self.kwargs.get('pk'),
                                   title=self.kwargs.get('slug'))
        return course

    template_name = 'course/course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CourseCategoryList(ListView):
    template_name = 'course/course-list.html'
    paginate_by = 9

    def get_queryset(self):
        global category_slug
        category_slug = self.kwargs['CategorySlug']
        category = CourseCategory.objects.filter(slug__iexact=category_slug).first()
        if category is None:
            raise Http404('صفحه مورد نظر یافت نشد')
        return Course.objects.get_course_by_category(category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = CourseCategory.objects.filter(slug__iexact=category_slug).first
        context['course_category'] = category
        return context


# render partial

def site_header(request):
    categories = CourseCategory.objects.get_active_category()
    context = {
        'categories': categories
    }
    return render(request, 'Shared/Header.html', context)
