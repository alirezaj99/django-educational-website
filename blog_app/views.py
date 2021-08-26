from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView
from .models import Blog, BlogTag
from .forms import CommentForm
from django.views.generic.edit import FormMixin
from django.contrib import messages
from extensions.utils import EmailService
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
class BlogList(ListView):
    def get_queryset(self):
        request = self.request
        search = request.GET.get('search')
        if search is not None:
            return Blog.objects.search(search)
        return Blog.objects.get_publish_blog()

    template_name = 'blog/blog-list.html'
    paginate_by = 8


class BlogDetail(FormMixin, DetailView):
    def get_object(self, **kwargs):
        blog = get_object_or_404(Blog.objects.get_publish_blog(), pk=self.kwargs.get('pk'),
                                 slug=self.kwargs.get('slug'))
        ip_address = self.request.user.ip_address
        if ip_address not in blog.hits.all():
            blog.hits.add(ip_address)
        return blog

    template_name = 'blog/blog-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # create comment
    def get_success_url(self):
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})

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
            self.obj.blog = self.object
            self.obj.user = self.request.user
            self.obj.active = True
            try:
                self.obj.parent_id = int(self.request.POST.get('parent_id'))
            except:
                self.obj.parent_id = None
            form.save()
            # send email
            author_email = self.obj.blog.author.email
            user_email = self.obj.user.email
            if author_email == user_email :
                author_email = False
                user_email = False
            parent_email = False
            if self.obj.parent :
                parent_email = self.obj.parent.user.email
                if parent_email in [author_email,user_email]:
                    parent_email = False    
            current_site = get_current_site(self.request)
            blog_url = f"{current_site}{reverse('blog:blog_detail' ,kwargs={'pk':self.obj.blog.pk,'slug':self.obj.blog.slug})}"
            blog_title = self.obj.blog.title        
            if author_email:
                subject = f'برای مقاله شما {blog_title} دیدگاه جدیدی ثبت شد'
                message = f'برای مقاله {blog_title} شما دیدگاه جدیدی توسط {self.obj.user} ثبت شده است.\n'
                EmailService.send_email(subject,[author_email],'email/course-comment.html',{'head_title':subject,'message':message,'blog_url':blog_url,'blog_title':blog_title})
            if parent_email:
                subject = f'کابر {self.obj.user} به دیدگاه شما در مقاله {self.obj.parent.blog.title} پاسخ داد'
                message = f'کابر {self.obj.user} به دیدگاه شما در مقاله {self.obj.parent.blog.title} پاسخ داد'
                EmailService.send_email(subject,[parent_email],'email/course-comment.html',{'head_title':subject,'message':message,'blog_url':blog_url,'blog_title':blog_title})
            # end send email
            messages.success(self.request,'دیدگاه شما با موفقیت ثبت شد. منتظر تایید باشید')
        return super(BlogDetail, self).form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,'عملیات ناموفق بود. دوباره تلاش کنید',extra_tags='error')
        return super(BlogDetail,self).form_invalid(form)



def sidebar_blog(request):
    blogs = Blog.objects.get_publish_blog()[:6]
    tags = BlogTag.objects.get_active_tag()[:20]
    context = {
        'blogs': blogs,
        'tags': tags,
    }
    return render(request, 'blog/sidebar-blog.html', context)
