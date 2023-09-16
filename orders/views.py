from unittest import result
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from cart.cart import Cart
from .forms import *
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from facades.views import InformationsForTemplate
# from suds.client import Client
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
# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://localhost:8000/orders/verify/'
#-----------------------------------------------------------------------------------
@login_required
def send_request(request,order_id,price):
    global amount , o_id
    amount = price
    o_id = order_id
    # result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, mobile, CallbackURL)
    if True:
        # result.Status == 100
        # return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        return verify(request)
    else:
        # return HttpResponse('Error code: ' + str(result.Status))
        pass
#-----------------------------------------------------------------------------------
def verify(request):
    # request.GET.get('Status') == 'OK'
    if True :
        result = 101
        # result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result == 100:
            # result.Status == 100
            order = Order.objects.get(id=o_id)
            order.paid = True
            order.save()
            cart = Cart(request)
            cart.clear()
            messages.success(request,'خرید با موفقیت انجام شد.','background-color: rgb(0, 190, 0);')
            return redirect('facades:dashboard')
        elif result == 101:
            # result.Status == 101
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
    
    return send_request(request,order.id,order.total_price)
#-----------------------------------------------------------------------------------