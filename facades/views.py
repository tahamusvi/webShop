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




    # return render(request,'facades/landing.html')
    return render(request,'facades/landing.html',{'products':news,'productsOfDiscount':discounted,'Categories' : Categories,
    'allCategories': allCategories,'wishlistAmount':wishlistAmount,'cart':cart,'covers':covers,'form':form})
#----------------------------------------------------------------------------------------------
def dashboard(request):

    #wishlist
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    #cart
    cart = Cart(request)




    # return render(request,'facades/landing.html')
    return render(request,'facades/dashboard.html',{'wishlistAmount':wishlistAmount,'cart':cart})
#----------------------------------------------------------------------------------------------
def contact(request):
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
    return render(request,'facades/contact.html',{'products':news,'productsOfDiscount':discounted,'Categories' : Categories,
    'allCategories': allCategories,'wishlistAmount':wishlistAmount,'cart':cart,'covers':covers,'form':form})
#----------------------------------------------------------------------------------------------
def aboutUs(request):
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
    return render(request,'facades/aboutUs.html',{'products':news,'productsOfDiscount':discounted,'Categories' : Categories,
    'allCategories': allCategories,'wishlistAmount':wishlistAmount,'cart':cart,'covers':covers,'form':form})
#----------------------------------------------------------------------------------------------
from django.core.mail import send_mail
from .forms import SurveyForm

def CreateSurvey(request):
    CreateSurvey = False
    form = SurveyForm()

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']

            surveyUser = Survey(
                name = name,
                email = email,
                phoneNumber = phone_number,
                title = title,
                text = text)
            surveyUser.save()

            CreateSurvey = True
    


    return render(request, 'facades/contact.html', {'form': form,'CreateSurvey':CreateSurvey})
#----------------------------------------------------------------------------------------------
