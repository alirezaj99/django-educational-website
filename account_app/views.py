from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from order_app.models import Order
from course_app.models import Course
from django.http import Http404


# Create your views here.

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
@login_required(login_url='account/login/')
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
