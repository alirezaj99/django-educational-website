"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # INSTALLED APPS
    'django_render_partial',
    'widget_tweaks',
    'ckeditor',
    'ckeditor_uploader',
    'azbankgateways',
    'captcha',
    # MY APPS
    'account_app',
    'course_app',
    'order_app',
    'cart_app',
    'index_app',
    'blog_app',
    'settings_app',
    'contact_app',
    'about_app',
    'templatetags',
    # DJANGO CLEANUP
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog_app.middleware.SaveIPAddressMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'base_tags': 'templatetags.base_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# if DEBUG:
#     STATICFILES_DIRS = [
#         BASE_DIR / "assets",
#     ]
# else:
#     STATIC_ROOT = (BASE_DIR / "static_cdn" / "static")

STATICFILES_DIRS = [
    BASE_DIR / 'assets',
]
STATIC_URL = '/static/'

STATIC_ROOT = (BASE_DIR / 'static_cdn' / 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = (BASE_DIR / 'static_cdn' / 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# User Model
AUTH_USER_MODEL = 'account_app.User'

# ckeditor
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

CKEDITOR_UPLOAD_PATH = "editor/uploads/"
CKEDITOR_FILENAME_GENERATOR = 'extensions.utils.get_filename'

# authenticate
LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# payment
AZ_IRANIAN_BANK_GATEWAYS = {
    'GATEWAYS': {
        # 'BMI': {
        #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
        #     'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
        #     'SECRET_KEY': '<YOUR SECRET CODE>',
        # },
        # 'SEP': {
        #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
        #     'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
        # },
        # 'ZARINPAL': {
        #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
        # },
        'IDPAY': {
            'MERCHANT_CODE': '6a7f99eb-7c20-4412-a972-6dfb7cd253a4',
            'METHOD': 'POST',  # GET or POST
            'X_SANDBOX': 1,  # 0 disable, 1 active
        },
        # 'ZIBAL': {
        #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
        # },
        # 'BAHAMTA': {
        #     'MERCHANT_CODE': '<YOUR MERCHANT CODE>',
        # },
        # 'MELLAT': {
        #     'TERMINAL_CODE': '<YOUR TERMINAL CODE>',
        #     'USERNAME': '<YOUR USERNAME>',
        #     'PASSWORD': '<YOUR PASSWORD>',
        # },
    },
    'DEFAULT': 'IDPAY',
    'CURRENCY': 'IRR',  # ??????????????
    'TRACKING_CODE_QUERY_PARAM': 'tc',  # ??????????????
    'TRACKING_CODE_LENGTH': 16,  # ??????????????
    'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',  # ??????????????
    'BANK_PRIORITIES': [
    ],
}

# email 
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# recaptcha
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')