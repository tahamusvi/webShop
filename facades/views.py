from django.shortcuts import render
from stuff.models import Product,Category
from .models import *
from accounts.forms import *
from cart.cart import Cart

#----------------------------------------------------------------------------------------------
def HomePage(request):
    print("--------------------------")
    # discounted stuff
    discounted = Product.objects.filter(available=True,discounted=True)
    # New stuff in website
    news = Product.objects.filter(available=True)
    news_list = [s.id for s in news if s.is_new][0:8]
    news = news.filter(id__in=news_list)
    # Categories
    Categories = Category.objects.filter(is_sub=False)[0:4]
    allCategories = Category.objects.filter(is_sub=False)
    #wishlist
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    #Covers
    covers = Cover.objects.all()
    #forms
    form = UserLoginForm
    #cart
    cart = Cart(request)
    CartAmount = cart.get_count()




    # return render(request,'facades/landing.html')
    return render(request,'facades/landing.html',{'products':news,'productsOfDiscount':discounted,'Categories' : Categories,
    'allCategories': allCategories,'wishlistAmount':wishlistAmount,'CartAmount':CartAmount,'covers':covers,'form':form})
#----------------------------------------------------------------------------------------------
