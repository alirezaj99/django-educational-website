from django.shortcuts import reverse,redirect, render
from django.http import Http404
from order_app.models import Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from cart_app.models import Cart

# Create your views here.

@login_required()
def go_to_gateway_view(request):

    if not str(request.META.get('HTTP_REFERER'))[-17:] in ["account/checkout/","/account/checkout"]:
        raise Http404("previous page")

    user = request.user
    cart = Cart.objects.get(user_id=user.id)
    cart_items = cart.items.all()

    if not cart_items:
        raise Http404()

    order = Order.objects.create(user_id=user.id,status='w',is_free=False,coupon_code=cart.coupon_code)
    
    for item in cart_items:
        order.items.create(course=item.course,price=item.price,discount=item.discount)

    order_items = order.items.all()

    if order.get_total_price() == 0 and order_items:
        order.is_free = True
        order.save()
        return redirect(reverse('order:call_back',kwargs={'order_id':order.id}))

    total_price = order.get_total_price()
    rial_total_price = total_price * 10
    # خواندن مبلغ از هر جایی که مد نظر است
    amount = rial_total_price
    # تنظیم شماره موبایل کاربر از هر جایی که مد نظر است
    user_mobile_number = ''  # اختیاری
    phone_number = user.profile.phone_number
    if phone_number:
        user_mobile_number = f'+98{phone_number}'
    factory = bankfactories.BankFactory()
    bank = factory.create()  # or factory.create(bank_models.BankType.BMI) or set identifier
    bank.set_request(request)
    bank.set_amount(amount)
    # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
    bank.set_client_callback_url(reverse('order:call_back',kwargs={'order_id':order.id}))
    if phone_number:
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
    # پرداخت برقرار کنید.
    bank_record = bank.ready()
    # هدایت کاربر به درگاه بانک
    return bank.redirect_gateway()


@login_required()
def callback_gateway_view(request, *args, **kwargs):
    user = request.user
    cart = Cart.objects.get(user_id=user.id)
    order = Order.objects.get(id=kwargs['order_id'])
    items = order.items.all()
    if order.is_free:
        order.status = 's'
        order.payment_date = timezone.now()
        order.save()
        for item in items:
            item.course.student.add(order.user)
        if not user.is_student:
            user.is_student = True
            user.save()
        for item in cart.items.all():
            item.delete()
        cart.coupon_code = None
        cart.save()
        return render(request, 'payment/payment-success.html', {'order_id': order.id})
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404()
    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404()

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        order.status = 's'
        order.payment_date = timezone.now()
        order.save()
        for item in items:
            item.course.student.add(order.user)
        if not user.is_student:
            user.is_student = True
            user.save()
        for item in cart.items.all():
            item.delete()
        cart.coupon_code = None
        cart.save()
        return render(request, 'payment/payment-success.html', {'order_id': order.id})

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    order.status = 'f'
    order.payment_date = timezone.now()
    order.save()
    for item in cart.items.all():
        item.delete()
    cart.coupon_code = None
    cart.save()
    return render(request, 'payment/payment-failed.html')
