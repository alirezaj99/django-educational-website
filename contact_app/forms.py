from django import forms
from .models import Contact

class ContactCreateForm(forms.ModelForm):
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