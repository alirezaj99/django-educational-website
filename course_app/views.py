from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView
from course_app.models import Course, CourseCategory
from django.http import Http404
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from blog_app.models import Blog
from settings_app.models import Settings


# Create your views here.

class CourseList(ListView):
    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if search is not None:
            return Course.objects.search(search)
        category = request.GET.get('categories')
        if category is not None:
            return Course.objects.get_course_by_category(category)
        return Course.objects.get_publish_course()

    template_name = 'course/course-list.html'
    paginate_by = 9


class CourseDetail(FormMixin, DetailView):
    def get_object(self):
        course = get_object_or_404(Course.objects.get_publish_course(), pk=self.kwargs.get('pk'),
                                   slug=self.kwargs.get('slug'))
        return course

    template_name = 'course/course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # create comment
    def get_success_url(self):
        return reverse('course:course_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.obj = form.save(commit=False)
            self.obj.course = self.object
            self.obj.user = self.request.user
            self.obj.active = False
            try:
                # id integer e.g. 15
                self.obj.parent_id = int(self.request.POST.get('parent_id'))
            except:
                self.obj.parent_id = None
            form.save()
        return super(CourseDetail, self).form_valid(form)


# render partial

def site_header(request):
    categories = CourseCategory.objects.get_active_category()
    settings = Settings.objects.first()
    email = settings.email
    instagram = settings.instagram
    youtube = settings.youtube
    twitter = settings.twitter
    context = {
        'categories': categories,
        'email': email,
        'instagram': instagram,
        'youtube': youtube,
        'twitter': twitter,
    }
    return render(request, 'Shared/Header.html', context)


def sidebar_course_list(request):
    categories = CourseCategory.objects.get_active_category()
    courses = Course.objects.get_publish_course()[:3]
    context = {
        'categories': categories,
        'courses': courses
    }
    return render(request, 'course/sidebar-course-list.html', context)


def header_references(request):
    settings = Settings.objects.first()
    icon = settings.site_favicon.url
    context = {
        'icon': icon
    }
    return render(request, 'Shared/_HeaderReferences.html', context)


def footer(request):
    categories = CourseCategory.objects.get_active_category()[:4]
    blogs = Blog.objects.get_publish_blog()[:8]
    settings = Settings.objects.first()
    instagram = settings.instagram
    youtube = settings.youtube
    twitter = settings.twitter
    site_title = settings.site_title
    context = {
        'categories': categories,
        'blogs': blogs,
        'instagram': instagram,
        'youtube': youtube,
        'twitter': twitter,
        'site_title': site_title,
    }
    return render(request, 'Shared/Footer.html', context)


def site_title_view(request):
    settings = Settings.objects.first()
    site_title = settings.site_title
    context = {
        'site_title': site_title,
    }
    return render(request, 'Shared/site_title.html', context)
