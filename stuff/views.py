from django.shortcuts import render,get_object_or_404
from .models import *
from accounts.forms import *
# from cart.forms import CartAddForm


# def home(request,slug=None):
#     products = Product.objects.filter(available=True)
#     categories = Category.objects.filter(is_sub=False)
#     if slug:
#         category = get_object_or_404(Category, slug=slug)
#         products = products.filter(category=category)
#     return render(request,'shop/home.html',{'products':products,'category':categories})
#-----------------------------------------------------------------------------------
def product_detail(request, slug,id):
    product = get_object_or_404(Product, id=id)
    # form = CartAddForm()

    category = product.category.all()[0]
    print(category)
    Suggested = category.products.all()[0:4]

    allCategories = Category.objects.filter(is_sub=False)


    return render(request,'stuff/product.html',{'product': product,'Suggested':Suggested,
    'allCategories': allCategories}) #,'form':form
#-----------------------------------------------------------------------------------
def Category_detail(request,slug,id):
    print("--------------------")
    category = get_object_or_404(Category, id=id)
    products = category.products.all()


    allCategories = Category.objects.filter(is_sub=False)

    #forms
    form = UserLoginForm

    #wishlist
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()

    return render(request,'stuff/bonePage.html',{'products': products,'category':category,
    'allCategories': allCategories,'wishlistAmount':wishlistAmount,'form':form})
#-----------------------------------------------------------------------------------
def showWishList(request):
    allCategories = Category.objects.filter(is_sub=False)
    products = request.user.wishlist.all()
    return render(request,'stuff/bonePage.html',{'products': products,'allCategories': allCategories})
