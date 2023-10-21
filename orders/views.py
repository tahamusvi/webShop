from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import BankAccount, Order, Address, OrderItem
from cart.cart import Cart
from .forms import CouponForm,receiptForm
from facades.views import InformationsForTemplate
from config.settings import merchant
from facades.models import ConfigShop
#------------------------------------------------------------------------------------------------
messages_dict = {
    "not_order" : 'جنین سفارشی در دیتابیس وجود ندارد.',
    "not_connected" : 'اتصال به درگاه ناموفق بود.',
    "too_long" : 'زمان بیش حد سپری شده برای اتصال به درگاه.',
    "not_success_connect" : 'اتصال ناموفق.',
    "success" : 'خرید با موفقیت انجام شد.',
    "payed" : 'پرداخت انجام شده بوده است.',
    "not_success_connect" : 'پرداخت ناموفق بود.',
    "not_upload" : 'آپلود با مشکل مواجه شد.',
    "success_upload" : "آپلود با موفقیت انجام شد. برای پیگیری سفارش به داشبورد مراجعه کنید.",
}

color_messages = {
    "error" : 'background-color: rgb(198, 2, 2);',
    "success" : 'background-color: rgb(0, 190, 0);',
    "gray" : 'background-color: rgb(108, 105, 105);',
}

#------------------------------------------------------------------------------------------------
@login_required
def detail(request,order_id):
    Info = InformationsForTemplate(request)
    form = CouponForm
    order = get_object_or_404(Order,id=order_id)

    Info['order'] = order
    Info['form'] = form

    if (order.user != request.user) and not(request.user.is_admin):
        return render(request,'facades/404.html', Info)
    
    if order.paid or order.receipt_bool:
        return render(request,'orders/trackOrders.html', Info)
    
    # return render(request,'orders/checkout.html', Info)
    return render(request,'facades/404.html', Info)
#------------------------------------------------------------------------------------------------
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
    site = ConfigShop.objects.get(current=True) 
    order = get_object_or_404(Order,id=order_id)
    if (order.user != request.user) and not(request.user.is_admin):
        return render(request,'facades/404.html',{'order':order})
    if order.paid :
        return render(request,'orders/factor.html',{'order':order,'site':site})
    return render(request,'facades/404.html',{'order':order})
#-----------------------------------------------------------------------------------

#Zarinpal
from django.http import HttpResponse
import requests
import json

if False:
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
        messages.success(request,messages_dict['not_order'],color_messages['error'])
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
        messages.success(request,messages_dict['not_connected'],color_messages['error'])
        return redirect('cart:detail')


    
    except requests.exceptions.Timeout:
        messages.success(request,messages_dict['too_long'],color_messages['error'])
        return redirect('cart:detail')
    except requests.exceptions.ConnectionError:
        messages.success(request,messages_dict['not_success_connect'],color_messages['error'])
        return redirect('cart:detail')
#-----------------------------------------------------------------------------------
def verify(request):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']

    global o_id
    try:
        user_order = Order.objects.get(id=o_id)
    except Order.DoesNotExist:
        messages.success(request,messages_dict['not_order'],color_messages['error'])
        return redirect('facades:home')

    amount = user_order.total_price()

    
    if(t_status == "NOK"):
        messages.success(request,messages_dict['not_success_connect'],color_messages['error'])
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
                messages.success(request,messages_dict['success'],color_messages['success'])
                return redirect('facades:dashboard')

        elif status == 101:
            cart = Cart(request)
            cart.clear()
            messages.success(request,messages_dict['payed'],color_messages['gray'])
            return redirect('facades:dashboard')

        else:
            messages.success(request,messages_dict['not_success_connect'],color_messages['error'])
            return redirect('cart:detail')
    else:
        messages.success(request,messages_dict['not_success_connect'],color_messages['error'])
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
@login_required
def order_create_receipt(request,address_id):
    if request.method == 'POST':
        cart = Cart(request)
        form = receiptForm(request.POST, request.FILES)
        if form.is_valid():
            order = Order.objects.create(user=request.user)

            order.address = Address.objects.get(id=address_id)
            for item in cart:
                OrderItem.objects.create(order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'])

            cd = form.cleaned_data
            order.receipt = cd['receipt']
            order.receipt_bool = True
            order.save()
            
            cart.clear()
            messages.success(request,messages_dict['success_upload'],color_messages['success'])
            return redirect("facades:home")
        else:
            messages.success(request,messages_dict["not_upload"],color_messages['error'])
            return order_create_receipt(request,address_id)

    Info = InformationsForTemplate(request)
    Info["receiptForm"] = receiptForm()
    Info["caddress"] = request.user.addresses.filter(current=True)[0]
    Info["hesab"] = BankAccount.objects.all()[::-1][0]
    
    return render(request,"orders/checkout.html",Info)
#-----------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
