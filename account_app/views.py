from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from .forms import LoginForm, CreateUserForm, ProfileUpdateForm, AvatarForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from order_app.models import Order
from course_app.models import Course
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView
from .models import User, Profile


# Create your views here.
class Register(CreateView):
    model = User
    form_class = CreateUserForm
    success_url = reverse_lazy('account:login')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        # messages.success(self.request, 'با موفقیت ثبت نام شدی', 'success')
        return super().form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, 'یه مشکلی هست ، ببین ارور چی میگه ! ( اعتبار سنجی یادت نره )', 'danger')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/courses/')

        return super().dispatch(request, *args, **kwargs)


class Login(LoginView):
    redirect_authenticated_user = reverse_lazy('course:course_list')
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('course:course_list')
        elif user.is_teacher:
            return reverse_lazy('course:course_list')
        else:
            return reverse_lazy('course:course_list')


@login_required(login_url='/account/login/')
def logout_view(request):
    logout(request)
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    else:
        return redirect('/courses')


# course
@login_required(login_url='/account/login/')
def add_course_to_order(request, *args, **kwargs):
    order = Order.objects.get(user_id=request.user.id, is_paid=False)
    if order is None:
        Order.objects.create(user_id=request.user.id, is_paid=False)
    course_id = kwargs['pk']
    course = Course.objects.get(id=course_id)
    if course is None or not course.status:
        raise Http404()
    item = order.items.filter(course_id=course_id).first()
    if item in order.items.all():
        # redirect to cart
        raise Http404()
    else:
        order.items.create(course_id=course_id, price=course.price)
    return redirect('/courses/')


@login_required(login_url='/account/login/')
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
        'avatar': profile.avatar, })
    if form.is_valid() and avatar_form.is_valid():
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.save()
        profile.phone_number = form.cleaned_data.get('phone_number')
        profile.bio = form.cleaned_data.get('bio')
        profile.website = form.cleaned_data.get('website')
        try:
            profile.avatar = avatar_form.cleaned_data.get('avatar')
        except:
            profile.avatar = profile.avatar
        profile.save()
        return HttpResponseRedirect(reverse('account:profile'))

    context = {
        'form': form,
        'avatar_form': avatar_form,
    }
    return render(request, 'account/edit-profile.html', context)
