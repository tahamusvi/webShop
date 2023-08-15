from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from cart.cart import Cart
from .forms import *
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
#-----------------------------------------------------------------------------------
@login_required
def order_create(request):
    cart = Cart(request)
    order = Order.objects.create(user=request.user)
    for item in cart:
        OrderItem.objects.create(order=order,
        product=item['product'],
        price=item['price'],
        quantity=item['quantity'])
    cart.clear()
    return redirect('orders:detail',order.id)
#-----------------------------------------------------------------------------------
@login_required
def detail(request,order_id):
    form = CouponForm
    order = get_object_or_404(Order,id=order_id)
    if (order.user != request.user) and not(request.user.is_admin):
        return render(request,'facades/404.html',{'order':order})
    if order.paid :
        return render(request,'orders/trackOrders.html',{'order':order})
    return render(request,'orders/checkout.html',{'order':order,'form':form})
#-----------------------------------------------------------------------------------
@require_POST
def coupon_apply(request,order_id):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
        except Coupon.DoesNotExist:
            messages.error(request,'this Coupon does not exist.','danger')
            return redirect('order:detail',order_id)
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect('orders:detail',order_id)

#-----------------------------------------------------------------------------------
def factor(request,order_id):
    form = CouponForm
    order = get_object_or_404(Order,id=order_id)
    if (order.user != request.user) and not(request.user.is_admin):
        return render(request,'facades/404.html',{'order':order})
    if order.paid :
        return render(request,'orders/factor.html',{'order':order})
    return render(request,'orders/checkout.html',{'order':order,'form':form})
#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
# from django.http import HttpResponse
# from django.shortcuts import redirect
# from suds.client import Client


# from django.contrib import messages






# MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
# client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
# description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
# email = 'email@example.com'  # Optional
# mobile = '09123456789'  # Optional
# # Important: need to edit for realy server.
# CallbackURL = 'http://localhost:8000/orders/verify/'


# @login_required
# def send_request(request,order_id,price):
#     global amount , o_id
#     amount = price
#     o_id = order_id
#     result = client.service.PaymentRequest(MERCHANT, amount, description, request.user.email, mobile, CallbackURL)
#     if result.Status == 100:
#         return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
#     else:
#         return HttpResponse('Error code: ' + str(result.Status))


# #-----------------------------------------------------------------------------------
# @login_required
# def verify(request):
#     if request.GET.get('Status') == 'OK':
#         result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
#         if result.Status == 100:
#             order = Order.objects.get(id=o_id)
#             order.paid = True
#             order.save()
#             messages.success(request,'Transaction was Successful')
#             return redirect('shop:home')
#         elif result.Status == 101:
#             return HttpResponse('Transaction submitted ')
#         else:
#             return HttpResponse('Transaction failed.')
#     else:
#         return HttpResponse('Transaction failed or canceled by user')
