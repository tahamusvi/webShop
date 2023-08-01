from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from stuff.models import Product
from .forms import CartAddForm
from django.views.decorators.http import require_POST



def detail(request):
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    cart = Cart(request)
    CartAmount = cart.get_count()
    print(CartAmount)

    return render(request,'cart/detail.html',{'cart':cart,'wishlistAmount':wishlistAmount,'CartAmount':CartAmount})
#-----------------------------------------------------------------------------------

@require_POST
def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    print(product)
    form = CartAddForm(request.POST)
    print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'])
    return redirect('cart:detail')

#-----------------------------------------------------------------------------------

def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:detail')
