from typing import FrozenSet
from django.db import models
from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Contact
from django.views.generic import CreateView
from .forms import ContactCreateForm
from django.contrib import messages
from settings_app.models import Settings
# Create your views here.

class ContactCreate(CreateView):
    model = Contact
    form_class = ContactCreateForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact:contact_create')

    def form_valid(self, form):
        messages.success(self.request,'پیام شما با موفقیت ارسال شد')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Settings.objects.first()
        context["address"] = setting.address 
        context["phone_number"] = setting.phone_number 
        context["email"] = setting.email 
        context["instagram"] = setting.instagram 
        context["twitter"] = setting.twitter 
        context["youtube"] = setting.youtube 
        return context
    