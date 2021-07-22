from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


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
