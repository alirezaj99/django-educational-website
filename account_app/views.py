from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .forms import LoginForm


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
