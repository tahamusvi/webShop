from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .cart import Cart
from stuff.models import Product
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from .forms import *
from orders.models import Coupon

@login_required
def detail(request):
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    cart = Cart(request)
    CartAmount = cart.get_count()
    print(CartAmount)


    return render(request,'cart/detail.html',{'cart':cart,'wishlistAmount':wishlistAmount,'CartAmount':CartAmount})
#-----------------------------------------------------------------------------------
def cart_add(request,product_id):
    if not request.user.is_authenticated:
        messages.success(request,'برای افزودن به سبد خرید ابتدا وارد حساب کاربری خود شوید.','background-color: rgb(198, 2, 2);')
        return redirect(request.META.get('HTTP_REFERER')) if(request.META.get('HTTP_REFERER')) else redirect('facades:home') #fix this bug in other situations
    

    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    
    if(request.method == "POST"):
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            if (product.warehouse - cd['quantity'] < 0):
                if(not product.available):
                    messages.error(request,'کالا در انبار موجود نیست!','background-color: rgb(198, 2, 2);')
                else:
                    messages.error(request,f"کالا تنها به تعداد {product.warehouse} عدد در انبار موجود است!",'background-color: rgb(198, 2, 2);')
                return redirect(request.META.get('HTTP_REFERER'))

            cart.add(product=product,quantity=cd['quantity'],color=request.POST.get('color'))
            product.change_available(int(cd['quantity']))
            messages.success(request,'با موفقیت کالا به سبد خرید اضافه شد.','background-color: rgb(0, 190, 0);')
        return redirect(request.META.get('HTTP_REFERER'))

    else:

        if(not product.available):
            messages.error(request,'کالا در انبار موجود نیست!','background-color: rgb(198, 2, 2);')
            return redirect(request.META.get('HTTP_REFERER'))
        
        cart.add(product=product,quantity=1)
        messages.success(request,'با موفقیت کالا به سبد خرید اضافه شد.','background-color: rgb(0, 190, 0);')
        return redirect(request.META.get('HTTP_REFERER'))
#-----------------------------------------------------------------------------------
def cart_remove(request,product_id_color):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id_color.split("-")[0])
    product.change_available(-1 * cart.remove(product_id_color))
    return redirect('cart:detail')
#-----------------------------------------------------------------------------------
@login_required
def checkout(request):
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    cart = Cart(request)
    # print(cart.discount)


    return render(request,'cart/checkout.html',{'cart':cart,'wishlistAmount':wishlistAmount,'caddress':request.user.addresses.filter(current=True)[0]})
#-----------------------------------------------------------------------------------
@require_POST
def coupon_apply(request):  
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
        except Coupon.DoesNotExist:
            messages.error(request,'this Coupon does not exist.','danger')
            return redirect('cart:checkout')
        cart = Cart(request)
        cart.apply_coupon(coupon)
        
    return redirect('cart:checkout')
