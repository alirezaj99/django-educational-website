from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordResetForm
from django.core.exceptions import ValidationError
from .models import Profile
from course_app.models import Course, Video
from captcha.fields import ReCaptchaV3,ReCaptchaField

class CreateUserForm(UserCreationForm):
    recaptcha = ReCaptchaField(
        label = 'تصویر امنیتی',
        widget=ReCaptchaV3(api_params={
            'h1':'fa'
        }),
        error_messages={
            'required': 'تصویر امنیتی را تایید کنید'
        }
    )
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise ValidationError('نام کاربری باید حداقل 7 کارکتر باشد')
        return username


class LoginForm(AuthenticationForm):
    recaptcha = ReCaptchaField(
        label = 'تصویر امنیتی',
        widget=ReCaptchaV3(api_params={
            'h1':'fa'
        }),
        error_messages={
            'required': 'تصویر امنیتی را تایید کنید'
        }
    )
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].required = True
        self.fields['password'].required = True

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

class ProfileUpdateForm(forms.ModelForm):
   
    class Meta:
        model = Profile
        fields = [
            'phone_number',
            'web_site',
            'bio',
            'avatar',
        ]

class UserUpdateForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]


class VideoCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(VideoCreate, self).__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)
        else:
            self.fields['course'].queryset = Course.objects.filter(teacher=user,status=True)
   

    class Meta:
        model = Video
        fields = [
            'title',
            'video',
            'position',
            'course',
            'description',
            'time',
            'publish_time',
        ]


class ResetForm(PasswordResetForm):
    recaptcha = ReCaptchaField(
            label = 'تصویر امنیتی',
            widget=ReCaptchaV3(api_params={
                'h1':'fa'
            }),
            error_messages={
                'required': 'تصویر امنیتی را تایید کنید'
            }
    )

    def __init__(self, *args, **kwargs):
        super(ResetForm, self).__init__(*args, **kwargs)
    

    def clean(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('کاربری با مشخصات وارد شده یافت نشد')
        return self.cleaned_data

class CoupenCodeForm(forms.Form):
    code = forms.CharField(max_length=50,label='کد تخفیف',required=True)