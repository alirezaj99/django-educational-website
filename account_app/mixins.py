from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone


class TeacherMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_teacher:
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
