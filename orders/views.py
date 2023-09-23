from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from cart.cart import Cart
from .forms import *
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from facades.views import InformationsForTemplate
from suds.client import Client
from config.settings import merchant
from django.http import HttpResponse
#-----------------------------------------------------------------------------------
@login_required
def detail(request,order_id):
    Info = InformationsForTemplate(request)
    form = CouponForm
    order = get_object_or_404(Order,id=order_id)

    Info['order'] = order
    Info['form'] = form

    if (order.user != request.user) and not(request.user.is_admin):
        return render(request,'facades/404.html', Info)
    
    if order.paid :
        return render(request,'orders/trackOrders.html', Info)
    
    # return render(request,'orders/checkout.html', Info)
    return render(request,'facades/404.html', Info)
#-----------------------------------------------------------------------------------
# @require_POST
# def coupon_apply(request,order_id):
#     now = timezone.now()
#     form = CouponForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
#         except Coupon.DoesNotExist:
#             messages.error(request,'this Coupon does not exist.','danger')
#             return redirect('order:detail',order_id)
#         order = Order.objects.get(id=order_id)
#         order.discount = coupon.discount
#         order.save()
#     return redirect('orders:detail',order_id)

#-----------------------------------------------------------------------------------
def factor(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    if (order.user != request.user) and not(request.user.is_admin):
        return render(request,'facades/404.html',{'order':order})
    if order.paid :
        return render(request,'orders/factor.html',{'order':order})
    return render(request,'facades/404.html',{'order':order})
#-----------------------------------------------------------------------------------

#Zarinpal
from django.http import HttpResponse
import requests
import json

if True:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


MERCHANT = merchant
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
# amount = 11000  # Rial / Required
description = "گیزموشاپ"  # Required
email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/orders/verify/'

o_id = 1450
user = None
#-----------------------------------------------------------------------------------
def send_request(request,order_id):
    global o_id
    o_id = order_id

    try:
        user_order = Order.objects.get(id=o_id)
    except Order.DoesNotExist:
        messages.success(request,'جنین سفارشی در دیتابیس وجود ندارد.','background-color: rgb(198, 2, 2);')
        return redirect('facades:home')

    amount = user_order.total_price()


    data = {
        "MerchantID": MERCHANT,
        "Amount": amount,
        "Description": description,
        "Phone": user_order.user.phoneNumber,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    try:
        response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

        
        response_dict = json.loads(response.text)
        status = response_dict['Status']
        authority = response_dict['Authority']


        if(status == 100):
            redirect_url = f"{ZP_API_STARTPAY}{authority}"
            return redirect(redirect_url)
        
        user_order.delete()
        messages.success(request,'اتصال به درگاه ناموفق بود.','background-color: rgb(198, 2, 2);')
        return redirect('cart:detail')


    
    except requests.exceptions.Timeout:
        messages.success(request,'زمان بیش حد سپری شده برای اتصال به درگاه.','background-color: rgb(198, 2, 2);')
        return redirect('cart:detail')
    except requests.exceptions.ConnectionError:
        messages.success(request,'اتصال ناموفق.','background-color: rgb(198, 2, 2);')
        return redirect('cart:detail')
#-----------------------------------------------------------------------------------
def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']

    global o_id
    try:
        user_order = Order.objects.get(id=o_id)
    except Order.DoesNotExist:
        messages.success(request,'جنین سفارشی در دیتابیس وجود ندارد.','background-color: rgb(198, 2, 2);')
        return redirect('facades:home')

    amount = user_order.total_price()

    
    if(t_status == "NOK"):
        messages.success(request,'پرداخت ناموفق بود.','background-color: rgb(198, 2, 2);')
        return redirect('cart:detail')
    
    elif(t_status == "OK"):
        data = {
            "MerchantID": MERCHANT,
            "Amount": amount,
            "Authority": t_authority,
        }
    
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        response_dict = json.loads(response.text)
        status = response_dict['Status']
        RefID = response_dict['RefID']

        if status == 100:
                order = Order.objects.get(id=o_id)
                order.paid = True
                order.ref_id = RefID
                order.authority = t_authority
                order.save()
                cart = Cart(request)
                cart.clear()
                messages.success(request,'خرید با موفقیت انجام شد.','background-color: rgb(0, 190, 0);')
                return redirect('facades:dashboard')

        elif status == 101:
            cart = Cart(request)
            cart.clear()
            messages.success(request,'پرداخت انجام شده بوده است.','background-color: rgb(108, 105, 105);')
            return redirect('facades:dashboard')

        else:
            messages.success(request,'پرداخت ناموفق بود.','background-color: rgb(198, 2, 2);')
            return redirect('cart:detail')
    else:
        messages.success(request,'پرداخت ناموفق بود.','background-color: rgb(198, 2, 2);')
        return redirect('cart:detail')
#-----------------------------------------------------------------------------------
@login_required
def order_create(request,address_id):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    order.address = Address.objects.get(id=address_id)
    for item in cart:
        OrderItem.objects.create(order=order,
        product=item['product'],
        price=item['price'],
        quantity=item['quantity'])
    order.save()
    
    return send_request(request,order.id)
#-----------------------------------------------------------------------------------
