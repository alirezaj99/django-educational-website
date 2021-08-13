from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from suds import Client
from order_app.models import Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify/'  # Important: need to edit for realy server.


@login_required()
def send_request(request):
    global total_price

    def get_mobile():
        if request.user.profile.phone_number:
            return f"0{request.user.profile.phone_number}"
        else:
            return mobile

    order = Order.objects.get(user_id=request.user.id, is_paid=False)
    total_price = order.get_total_price()
    if order and order.items.all():
        result = client.service.PaymentRequest(MERCHANT, total_price, description, request.user.email, get_mobile(),
                                               CallbackURL)
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    else:
        return redirect('course:course_list')


@login_required()
def verify(request):
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], total_price)
        if result.Status == 100:
            order = Order.objects.get(user_id=request.user.id, is_paid=False)
            order.is_paid = True
            order.payment_date = timezone.now()
            for item in order.items.all():
                item.course.student.add(order.user)
            order.save()
            Order.objects.create(user_id=order.user.id, is_paid=False)
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
