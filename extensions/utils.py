from . import jalali
from django.utils import timezone
from random import randint
import uuid
from django import forms
from captcha.fields import ReCaptchaField,ReCaptchaV3
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
# jalali converter

def jalali_converter(time):
    jmonth = ["فروردین",
              "اردیبهشت",
              "خرداد",
              "تیر",
              "مرداد",
              "شهریور",
              "مهر",
              "آبان",
              "آذر",
              "دی",
              "بهمن",
              "اسفند"]
    time = timezone.localtime(time)
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    def get_minute():
        if len(str(time.minute)) == 1:
            return f'0{time.minute}'
        else:
            return time.minute

    def get_hour():
        if len(str(time.hour)) == 1:
            return f'0{time.hour}'
        else:
            return time.hour

    output = "{}  {}  {} , ساعت {} : {}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        get_minute(),
        get_hour(),
    )

    return output


def jalali_converter_date(time):
    jmonth = ["فروردین",
              "اردیبهشت",
              "خرداد",
              "تیر",
              "مرداد",
              "شهریور",
              "مهر",
              "آبان",
              "آذر",
              "دی",
              "بهمن",
              "اسفند"]
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = "{}  {}  {} ".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.minute,
        time.hour,

    )

    return output


def jalali_converter_year(time):
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    output = "{}".format(
        time_to_list[0],

    )

    return output


def jalali_converter_month(time):
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    output = "{}".format(
        time_to_list[1],

    )

    return output


def jalali_converter_day(time):
    time_to_str = "{},{},{}".format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    output = "{}".format(
        time_to_list[2],

    )

    return output


# ckeditor
def get_filename(filename, request):
    uniq_str = uuid.uuid4().hex[:10]
    return f'image-{uniq_str.upper()}-{randint(99, 99999)}'

# model forms with recaptcha 

class ModelFormWithRecaptcha(forms.ModelForm):
    recaptcha = ReCaptchaField(
        label = 'تصویر امنیتی',
        widget=ReCaptchaV3(api_params={
            'h1':'fa'
        }),
        error_messages={
            'required': 'تصویر امنیتی را تایید کنید'
        }
    )

# email service

class EmailService:

    @staticmethod
    def send_email(subject,to,template_name,context) :
        html_message = render_to_string(template_name,context)
        plain_message  = strip_tags(html_message)
        send_mail(subject,plain_message,settings.EMAIL_HOST_USER,to,html_message=html_message)