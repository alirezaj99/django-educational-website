from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from .forms import LoginForm, CreateUserForm, ProfileUpdateForm, AvatarForm, ResetForm,VideoCreate,PasswordResetForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from order_app.models import Order, OrderItem
from course_app.models import Course,Video
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView
from .models import User, Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import (TeacherMixin, CourseValidMixin, CourseFieldMixin, BlogCreateFieldMixin, BlogCreateValidMixin)
from blog_app.models import Blog
from django.contrib import messages

# register view
class Register(CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('account:login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        messages.success(self.request,'ثبت نام با موفقیت انجام شد. وارد شوید')
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, 'یه مشکلی هست ، ببین ارور چی میگه ! ( اعتبار سنجی یادت نره )', 'danger')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)


# login view
class Login(LoginView):
    redirect_authenticated_user = reverse_lazy('course:course_list')
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user
        try:
            if self.request.GET.get('next'):
                return resolve_url(f"http://127.0.0.1:8000{self.request.GET.get('next')}")
                # todo : set site url
            elif user.is_superuser:
                return reverse_lazy('account:profile')
            elif user.is_teacher:
                return reverse_lazy('account:profile')
            else:
                return reverse_lazy('account:profile')
        except:
            return reverse_lazy('account:profile')


# logout view
@login_required()
def logout_view(request):
    logout(request)
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect('/courses')


# password change view
class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:profile')

    def form_valid(self,form):
        messages.success(self.request,'رمز عبور شما با موفقیت تغییر کرد')
        return super().form_valid(form)


# course
@login_required()
def add_course_to_order(request, *args, **kwargs):
    user_courses = request.user.student_courses.get_publish_course()
    order = Order.objects.get(user_id=request.user.id, is_paid=False)
    if order is None:
        Order.objects.create(user_id=request.user.id, is_paid=False)
    course_id = kwargs['pk']
    course = Course.objects.get(id=course_id)
    if course in user_courses:
        return redirect('account:my_courses')
    if course is None or not course.status:
        raise Http404()
    item = order.items.filter(course_id=course_id).first()
    if item in order.items.all():
        return redirect('account:cart')
    else:
        if course.discount and 0 < course.discount <= 100 and course.price > 0:
            discount = course.discount
        else:
            discount = None
        order.items.create(course_id=course_id, price=course.price, discount=discount)
    return redirect('account:cart')


@login_required()
def delete_course_from_order(request, *args, **kwargs):
    item_id = kwargs['pk']
    if item_id is not None:
        item = get_object_or_404(OrderItem, pk=item_id)
        if item is not None:
            item.delete()
            return redirect('account:cart')
    raise Http404()


@login_required()
def profile_update(request):
    user = User.objects.get(pk=request.user.pk)
    profile = Profile.objects.get(user_id=request.user.id)
    form = ProfileUpdateForm(request.user, request.POST or None, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': f'0{profile.phone_number}',
        'bio': profile.bio,
        'web_site': profile.web_site,
    })
    avatar_form = AvatarForm(request.POST or None, request.FILES, initial={
        'avatar': profile.avatar})
    if form.is_valid() and avatar_form.is_valid():
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        profile.phone_number = form.cleaned_data.get('phone_number')
        profile.bio = form.cleaned_data.get('bio')
        profile.web_site = form.cleaned_data.get('web_site')
        try:
            profile.avatar = avatar_form.cleaned_data.get('avatar')
        except:
            profile.avatar = profile.avatar
        profile.save()
        messages.success(request,'عملیات با موفقیت انجام شد')
        return HttpResponseRedirect(reverse('account:profile'))

    context = {
        'form': form,
        'avatar_form': avatar_form,
    }
    return render(request, 'account/profile.html', context)


class Cart(LoginRequiredMixin, ListView):
    def get_queryset(self):
        order = Order.objects.get(user_id=self.request.user.id, is_paid=False)
        items = order.items.all()
        return items

    template_name = 'account/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(user_id=self.request.user.id, is_paid=False)
        return context


class MyCourses(LoginRequiredMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        courses = user.student_courses.get_publish_course().order_by('-course_app_course_student.id')
        return courses

    template_name = 'account/my-courses.html'


class CourseAdd(LoginRequiredMixin, CourseValidMixin, CourseFieldMixin, TeacherMixin, CreateView):
    model = Course
    template_name = 'account/course-add.html'
    success_url = reverse_lazy('account:teacher_courses')

    def form_valid(self,form):
        messages.success(self.request,'درخواست شما با موفقیت ثبت شد')
        return super().form_valid(form)

class VideoAdd(LoginRequiredMixin,TeacherMixin,CreateView):
    model = Video
    form_class = VideoCreate
    template_name = 'account/video-add.html'
    success_url = reverse_lazy('account:teacher_courses')

    def form_valid(self,form):
        messages.success(self.request,'درخواست شما با موفقیت ثبت شد')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(VideoAdd, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class TeacherCourses(LoginRequiredMixin, TeacherMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        # courses = Course.objects.filter(teacher=user)
        courses = user.teacher_courses.all()
        return courses

    template_name = 'account/teacher-courses.html'


class MyComment(LoginRequiredMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        comments = user.comments.all()
        return comments

    template_name = 'account/my-comment.html'


class TeacherBlogs(LoginRequiredMixin, TeacherMixin, ListView):
    def get_queryset(self):
        user = self.request.user
        blogs = user.blogs.all()
        return blogs

    template_name = 'account/teacher-blogs.html'


class BlogCreate(LoginRequiredMixin, TeacherMixin, BlogCreateFieldMixin, BlogCreateValidMixin, CreateView):
    model = Blog
    success_url = reverse_lazy('account:teacher_blogs')
    template_name = 'account/blog-create.html'

    def form_valid(self,form):
        messages.success(self.request,'درخواست شما با موفقیت ثبت شد')
        return super().form_valid(form)


class PaymentList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        order = Order.objects.filter(user_id=self.request.user.id, is_paid=True)
        return order

    template_name = 'account/payment-list.html'


class PaymentDetail(LoginRequiredMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        order = get_object_or_404(Order.objects.filter(user_id=self.request.user.id, is_paid=True),
                                  pk=pk)
        return order

    template_name = 'account/payment-detail.html'


class PasswordReset(PasswordResetView):
    success_url = reverse_lazy('account:login')
    form_class = ResetForm

    def form_valid(self, form):
        messages.success(self.request,'لینک بازیابی رمز به ایمیل شما ارسال شد')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)

class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        messages.success(self.request,'بازیابی رمز عبور با موفقیت انجام شد. وارد شوید')
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        return super().dispatch(request, *args, **kwargs)