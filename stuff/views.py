from django.shortcuts import render,get_object_or_404
from .models import *
from accounts.forms import *
from accounts.forms import UserLoginForm
from django.db.models import Q
from django.core.paginator import Paginator
from cart.cart import Cart
#-----------------------------------------------------------------------------------
pagination_amount = 12
#-----------------------------------------------------------------------------------
def product_detail(request, slug,id):
    form = UserLoginForm
    product = get_object_or_404(Product, id=id)
    # form = CartAddForm()

    category = product.category.all()[0]
    print(category)
    Suggested = category.products.all()[0:4]

    allCategories = Category.objects.filter(is_sub=False)



    #wishlist
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    #cart
    cart = Cart(request)
    CartAmount = cart.get_count()


    return render(request,'stuff/product.html',{'product': product,'Suggested':Suggested,
    'allCategories': allCategories,'wishlistAmount':wishlistAmount,'cart':cart,'form':form}) 
#-----------------------------------------------------------------------------------
import random
from faker import Faker
def CopyObjects(request):
    fake = Faker()

    num_products = 100
    categories = Category.objects.all()

    products = Product.objects.all()

    for i in range(num_products):
        p = random.choice(products)
        
        product = Product()
        product.name = p.name + " " + fake.name()
        product.slug = fake.slug()
        product.image = p.image
        product.image2 = p.image2
        product.image3 = p.image3
        product.description = fake.text()
        product.price = random.randint(1000, 10000)
        product.available = True
        product.save()
        product.category.add(random.choice(categories))

        product.save()
    

#-----------------------------------------------------------------------------------
def Category_detail(request,id,page):
    print("--------------------")
    category = get_object_or_404(Category, id=id)
    products = category.products.all()

    paginator = Paginator(products, pagination_amount)
    products = paginator.get_page(page)


    allCategories = Category.objects.filter(is_sub=False)


    brands = Brand.objects.all()
    #forms
    form = UserLoginForm

    #wishlist
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    #cart
    cart = Cart(request)
    CartAmount = cart.get_count()

    return render(request,'stuff/bonePage.html',{'products': products,'category':category,'paginator':paginator,
    'allCategories': allCategories,'brands':brands,'wishlistAmount':wishlistAmount,'cart':cart,'form':form})
#-----------------------------------------------------------------------------------
def showWishList(request,page):
    wishlistProducts = request.user.wishlist.all()

    paginator = Paginator(wishlistProducts, pagination_amount)
    products = paginator.get_page(page)

    brands = Brand.objects.all()
    allCategories = Category.objects.filter(is_sub=False)
    #wishlist
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    #cart
    cart = Cart(request)
    CartAmount = cart.get_count()

    return render(request,'stuff/bonePage.html',{'products': products,'num_pages':paginator.num_pages,'paginator':paginator,
    'allCategories': allCategories,'brands':brands,'wishlistAmount':wishlistAmount,'cart':cart})
#-----------------------------------------------------------------------------------
def product_search(request,page):
    filter_price_option = -1

    if(request.method == "POST"):
       print("----3----------------------------")
       print(request.POST)

       filter_price_option = int(request.POST["filter-price"])

       filter_price_high = 250 * 2 ** (filter_price_option - 1) * 1000
       filter_price_low = filter_price_high // 2

       if(filter_price_option == 1):
           filter_price_low = 0

       if(filter_price_option == 5):
           filter_price_high = 10000000
           filter_price_low = 2000000
        

    
    
    query = request.GET.get('query')
    product_list = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if(filter_price_option != -1):
        product_list = product_list.filter(price__gte=filter_price_low, price__lte=filter_price_high) 
        

    paginator = Paginator(product_list, pagination_amount)
    products = paginator.get_page(page)



    brands = Brand.objects.all()
    allCategories = Category.objects.filter(is_sub=False)

    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()

    #cart
    cart = Cart(request)
    CartAmount = cart.get_count()


    return render(request, 'stuff/bonePage.html', {'products': products,'query':query,'num_pages':paginator.num_pages,'paginator':paginator,
    'allCategories': allCategories,'brands':brands,'wishlistAmount':wishlistAmount,'cart':cart})
#-----------------------------------------------------------------------------------