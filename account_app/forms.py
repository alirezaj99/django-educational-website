from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Profile
from django.core import validators


class CreateUserForm(UserCreationForm):
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


class ProfileUpdateForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        # self.fields['phone_number'].required = False
        # self.fields['web_site'].required = False
        # self.fields['bio'].required = False

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={}),
        label="نام",
        validators=[validators.MaxLengthValidator(150, "نام نباید بیشتر از 150 کارکتر باشد")]
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={}),
        label="نام خانوادگی",
        validators=[validators.MaxLengthValidator(150, "نام خانوادگی نباید بیشتر از 150 کارکتر باشد")]
    )

    phone_number = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={}),
        label="شماره تماس", required=False,
    )
    web_site = forms.URLField(
        widget=forms.URLInput(
            attrs={}),
        label="وب سایت", required=False,
    )

    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={}),
        label="متن نظر", required=False,
        validators=[validators.MaxLengthValidator(700, "بیوگرافی نباید بیشتر از 700 کارکتر باشد")]
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        profile = Profile.objects.get(user_id=self.user.id)
        profiles = Profile.objects.filter(phone_number=phone_number)
        if profiles.exists() and phone_number != profile.phone_number:
            raise ValidationError("این شماره تماس قبلا ثبت شده است.")
        return phone_number


class AvatarForm(forms.Form):
    avatar = forms.ImageField(
        label="تصویر پروفایل", required=False
    )
