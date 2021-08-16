from django.shortcuts import reverse, redirect
from django.http import HttpResponse, Http404
from order_app.models import Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from azbankgateways import bankfactories, models as bank_models, default_settings as settings


# Create your views here.

@login_required()
def go_to_gateway_view(request):
    user = request.user
    order = Order.objects.get(user_id=user.id, is_paid=False)
    if not order.items.all():
        return redirect('course:course_list')
    items = order.items.all()

    if order.get_total_price() == 0 and items:
        order.is_paid = True
        order.payment_date = timezone.now()
        for item in items:
            item.course.student.add(order.user)
        order.save()
        Order.objects.create(user_id=order.user.id, is_paid=False)
        if not user.is_student:
            user.is_student = True
            user.save()
        return HttpResponse("پرداخت با موفقیت انجام شد.")
    total_price = order.get_total_price()
    rial_total_price = total_price * 10
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = rial_total_price
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = '+989999999999'  # اختیاری
    phone_number = user.profile.phone_number
    if phone_number:
        user_mobile_number = f'+98{phone_number}'
    factory = bankfactories.BankFactory()
    bank = factory.create()  # or factory.create(bank_models.BankType.BMI) or set identifier
    bank.set_request(request)
    bank.set_amount(amount)
    # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
    bank.set_client_callback_url(reverse('order:call_back'))
    if phone_number:
        bank.set_mobile_number(user_mobile_number)  # اختیاری

    # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
    # پرداخت برقرار کنید.
    bank_record = bank.ready()

    # هدایت کاربر به درگاه بانک
    return bank.redirect_gateway()


@login_required()
def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        user = request.user
        order = Order.objects.get(user_id=user.id, is_paid=False)
        order.is_paid = True
        order.payment_date = timezone.now()
        items = order.items.all()
        for item in items:
            item.course.student.add(order.user)
        order.save()
        Order.objects.create(user_id=order.user.id, is_paid=False)
        if not user.is_student:
            user.is_student = True
            user.save()
        return HttpResponse("پرداخت با موفقیت انجام شد.")

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse(
        "پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")
