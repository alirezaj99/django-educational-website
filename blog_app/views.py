from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Blog


# Create your views here.
class BlogList(ListView):
    def get_queryset(self):
        return Blog.objects.get_publish_blog()

    template_name = 'blog/blog-list.html'
    paginate_by = 8


class BlogDetail(DetailView):
    def get_object(self, **kwargs):
        blog = get_object_or_404(Blog.objects.get_publish_blog(), pk=self.kwargs.get('pk'),
                                 slug=self.kwargs.get('slug'))
        return blog

    template_name = 'blog/blog-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def sidebar_blog(request):
    blogs = Blog.objects.get_publish_blog()[:6]
    context = {
        'blogs': blogs
    }
    return render(request, 'blog/sidebar-blog.html', context)
