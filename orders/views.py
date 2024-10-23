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
from stuff.models import Product
from config.settings import SMS_PASSWORD,ADMIN_PHONE
from ippanel import Client
#------------------------------------------------------------------------------------------------
messages_dict = {
    "not_order" : 'جنین سفارشی در دیتابیس وجود ندارد.',
    "not_connected" : ' اتصال به درگاه ناموفق بود. لطفا از پرداخت کارت به کارت استفاده نمایید.',
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

    if order.user != request.user:
        if not(request.user.is_admin):
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
        return render(request,'facades/404.html',{'order':order,'site':site})
    if order.paid :
        return render(request,'orders/factor.html',{'order':order,'site':site})
    return render(request,'facades/404.html',{'order':order,'site':site})
#-----------------------------------------------------------------------------------

#Zarinpal
from django.http import HttpResponse
import requests
import json


MERCHANT = merchant
gateway_send= 'https://bitpay.ir/payment/gateway-send'
gateway_second = 'https://bitpay.ir/payment/gateway-result-second'

# gateway_send_test= 'https://bitpay.ir/payment-test/gateway-send'
# gateway_second_test = 'https://bitpay.ir/payment-test/gateway-result-second'
# amount = 11000  # Rial / Required
description = "گیزموشاپ"  # Required
email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'https://vahdat-sh.ir/orders/verify/'

o_id = 1450
user = None

merchant_test = "adxcv-zzadq-polkjsad-opp13opoz-1sdf455aadzmck1244567"
merchant2 = "03e8b-e1775-76e11-362e1-7b4f39c1867976ae3974c0170c2e"
#-----------------------------------------------------------------------------------
def send_request(request,order_id):
    user = request.user
    
    user.redirect = True
    user.order_id = order_id
    
    user.save()
    return redirect('facades:home')
    
#-----------------------------------------------------------------------------------
def verify(request):

    trans_id = request.GET.get('trans_id')
    id_get = request.GET['id_get']


    data = {}

    data['trans_id'] = trans_id
    data['id_get'] = id_get
    data['api'] = merchant2
    data['json'] = 1

    response = requests.post(gateway_second, data)

    response_dict = response.json()


    status = response_dict['status']
    amount_dar = response_dict['amount']
    cardNum = response_dict['cardNum']
    order_id = response_dict['factorId']

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        messages.success(request,messages_dict['not_order'],color_messages['error'])
        return redirect('facades:home')

    amount = order.total_price()

    # if(amount == amount_dar):
    #     print("ok")

    if(status in [-1,-2,-3,-4]):
        messages.success(request,messages_dict['not_success_connect'],color_messages['error'])
        return redirect('cart:detail')

    elif(status == 1):
        order.paid = True
        order.ref_id = id_get
        order.authority = trans_id
        order.save()
        cart = Cart(request)
        cart.clear()
        #change amount of wearhouse

        # send sms to Customer
        user = request.user
        sms = Client(SMS_PASSWORD)

        pattern_values = {
            "username": str(user.full_name),
            "order-code": str(order.get_order_number())
        }

        message_id = sms.send_pattern(
            "bxve3ieo3u6ywg2",    # pattern code
            "+983000505",      # originator
            f"98{user.phoneNumber[1:]}",  # recipient
            pattern_values,  # pattern values
        )
        print(f"message sended to customer id: {message_id}")


        # send sms to Admin
        message_id = sms.send_pattern(
            "71hahbwqbep8qw5",    # pattern code
            "+983000505",      # originator
            f"98{ADMIN_PHONE[1:]}",  # recipient
            {"order-code": str(order.get_order_number()), },  # pattern values
        )

        print(f"message sended to admin id: {message_id}")




        
        messages.success(request,messages_dict['success'],color_messages['success'])
        return redirect('administratorship:dashboard')

    elif status == 11:
        cart = Cart(request)
        cart.clear()
        messages.success(request,messages_dict['payed'],color_messages['gray'])
        return redirect('administratorship:dashboard')
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
                product = get_object_or_404(Product,id=int(item['product_id']))
                product.change_available(int(item['quantity']))

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

