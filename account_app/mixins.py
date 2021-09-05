from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone


class TeacherMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_teacher or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')


class CourseFieldMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_teacher:
            self.fields = [
                'title',
                'image',
                'description',
                'price',
                'discount',
                'categories',
                'tags',
                'level',
                'language',
            ]


        else:
            raise Http404('این صفحه برای شما در دسترس نیست')

        return super().dispatch(request, *args, **kwargs)


class CourseValidMixin():
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        self.obj.teacher = self.request.user
        self.obj.is_finish = False
        self.obj.status = False
        self.obj.publish_time = timezone.now()
        return super().form_valid(form)


class BlogCreateFieldMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["author",
                           "title",
                           "description",
                           "image",
                           "tags",
                           "hits",
                           "status",
                           "publish_time", ]
        elif request.user.is_teacher:
            self.fields = ["title",
                           "description",
                           "tags",
                           "image",
                           "publish_time",
                           ]

        else:
            raise Http404('این صفحه برای شما در دسترس نیست')

        return super().dispatch(request, *args, **kwargs)


class BlogCreateValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = False
        return super().form_valid(form)
