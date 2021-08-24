from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
from extensions.utils import ModelFormWithRecaptcha

class ContactCreateForm(ModelFormWithRecaptcha):
    def __init__(self,*args, **kwargs):
        super(ContactCreateForm,self).__init__(*args, **kwargs)
    
    class Meta:
        model= Contact
        fields=[
            'name',
            'email',
            'phone_number',
            'subject',
            'message',
        ]

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not 16 > len(str(phone_number)) > 7 :
            raise ValidationError('شماره تماس باید بین 8 تا 15 کاراکتر باشد')
        return phone_number