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
        try :
            int(phone_number)
        except:
            raise ValidationError('لطفا عدد وارد کنید')

        if len(phone_number) < 8 or len(phone_number) > 11 :
            raise ValidationError('شماره تماس باید بین 8 تا 11 کاراکتر باشد')
        return phone_number