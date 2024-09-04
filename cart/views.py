from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .cart import Cart
from stuff.models import Product
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import CartAddForm
from accounts.forms import AddressForm
from facades.models import ConfigShop
#------------------------------------------------------------------------------------------------
messages_dict = {
    "not_logined" : 'برای افزودن به سبد خرید ابتدا وارد حساب کاربری خود شوید.',
    "not_available" : 'کالا در انبار موجود نیست!',
    "not_available_amount" : 'کالا تنها به تعداد d عدد در انبار موجود است!',
    "added_cart" : 'با موفقیت کالا به سبد خرید اضافه شد.',
    "too_many_ordered" : 'شما تمام موجودی انبار را سفارش داده اید.'
}

color_messages = {
    "error" : 'background-color: rgb(198, 2, 2);',
    "success" : 'background-color: rgb(0, 190, 0);',
    "gray" : 'background-color: rgb(108, 105, 105);',

}
#------------------------------------------------------------------------------------------------
@login_required
def detail(request):
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    cart = Cart(request)
    CartAmount = cart.get_count()

    site = ConfigShop.objects.get(current=True)
    return render(request,'cart/detail.html',{'cart':cart,'wishlistAmount':wishlistAmount,'CartAmount':CartAmount,'site':site})
#-----------------------------------------------------------------------------------
def cart_add(request,product_id):
    if not request.user.is_authenticated:
        messages.success(request,messages_dict['not_logined'],color_messages['error'])
        return redirect(request.META.get('HTTP_REFERER')) if(request.META.get('HTTP_REFERER')) else redirect('facades:home')
    

    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    
    if(request.method == "POST"):
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            if (product.warehouse - cd['quantity'] < 0):
                if(not product.available):
                    messages.error(request,messages_dict['not_available'],color_messages['error'])
                else:
                    messages.error(request,messages_dict['not_available_amount'].replace("d",str(product.warehouse)),color_messages['error'])
                return redirect(request.META.get('HTTP_REFERER')) if(request.META.get('HTTP_REFERER')) else redirect('facades:home')

            print(cart.amount_product(product.id))
            if(product.warehouse == cart.amount_product(product.id)):
                messages.error(request,messages_dict['too_many_ordered'],color_messages['error'])
                return redirect(request.META.get('HTTP_REFERER')) if(request.META.get('HTTP_REFERER')) else redirect('facades:home')

            cart.add(product=product,quantity=cd['quantity'],color=request.POST.get('color'))
            # product.change_available(int(cd['quantity']))
            product.ordered_increase(int(cd['quantity']))
            messages.success(request,messages_dict['added_cart'],color_messages['success'])
        return redirect(request.META.get('HTTP_REFERER')) if(request.META.get('HTTP_REFERER')) else redirect('facades:home')

    else:

        if(not product.available):
            messages.error(request,'کالا در انبار موجود نیست!',color_messages['error'])
            return redirect(request.META.get('HTTP_REFERER')) if(request.META.get('HTTP_REFERER')) else redirect('facades:home')
        
        cart.add(product=product,quantity=1)
        messages.success(request,messages_dict['added_cart'],'background-color: rgb(0, 190, 0);')
        return redirect(request.META.get('HTTP_REFERER')) if(request.META.get('HTTP_REFERER')) else redirect('facades:home')
#-----------------------------------------------------------------------------------
def cart_remove(request,product_id_color):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id_color.split("-")[0])
    # product.change_available(-1 * cart.remove(product_id_color))
    product.ordered_increase(-1 * cart.remove(product_id_color))
    return redirect('cart:detail')
#-----------------------------------------------------------------------------------
@login_required
def checkout(request):
    cart = Cart(request)
    way_optin = request.user.last_send_way
    # print(way_ooptin)
    price_way = 0
    for item in cart:
        price_way += item['product'].transit_price * item['quantity']

    total = cart.get_total_price() + price_way

    site = ConfigShop.objects.get(current=True) 
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    addressForm = AddressForm()
    if(request.user.addresses.filter(current=True).count() > 0):
        has_address = True
        current_address = request.user.addresses.filter(current=True)[0]
    else:
        has_address = False
        current_address = None
    

    return render(request,'cart/checkout.html',{'total':total,'price_way':price_way,'cart':cart,'wishlistAmount':wishlistAmount,'has_address':has_address,'caddress':current_address,"addressForm":addressForm,'site':site})
#-----------------------------------------------------------------------------------
# @require_POST
# def coupon_apply(request):  
#     now = timezone.now()
#     form = CouponForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupon = Coupon.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
#         except Coupon.DoesNotExist:
#             messages.error(request,'this Coupon does not exist.','danger')
#             return redirect('cart:checkout')
#         cart = Cart(request)
#         cart.apply_coupon(coupon)
        
#     return redirect('cart:checkout')
