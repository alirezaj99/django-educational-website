from . import jalali
from django.utils import timezone
from random import randint


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
