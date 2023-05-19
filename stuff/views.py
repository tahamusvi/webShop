from django.shortcuts import render,get_object_or_404
from .models import *
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


    return render(request,'stuff/product.html',{'product': product,'Suggested':Suggested}) #,'form':form
