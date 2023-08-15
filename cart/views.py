from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .cart import Cart
from stuff.models import Product
from .forms import CartAddForm
from django.views.decorators.http import require_POST
from django.contrib import messages


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
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    if(request.method == "POST"):
        
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,quantity=cd['quantity'])
            messages.success(request,'با موفقیت کالا به سبد خرید اضافه شد.','background-color: #00ac09;')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        cart.add(product=product,quantity=1)
        messages.success(request,'با موفقیت کالا به سبد خرید اضافه شد.','background-color: #00ac09;')
        return redirect(request.META.get('HTTP_REFERER'))


#-----------------------------------------------------------------------------------

def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:detail')
