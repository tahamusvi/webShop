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
    'allCategories': allCategories,'wishlistAmount':wishlistAmount,'CartAmount':CartAmount,'covers':covers,'form':form})
#----------------------------------------------------------------------------------------------
from django.core.mail import send_mail
from .forms import SurveyForm

def CreateSurvey(request):
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
            
            # # ارسال ایمیل
            # message = f'نام: {name}\nایمیل: {email}\nشماره موبایل: {phone_number}\nموضوع: {title}\nمتن پیام: {text}'
            # send_mail(
            #     'پیام از طرف فرم تماس با ما',
            #     message,
            #     'example@example.com', # ایمیل شخص ارسال کننده
            #     ['example@example.com'], # ایمیل شخص دریافت کننده
            #     fail_silently=False,
            # )

            # ارسال پیام thank you
            # return render(request, 'thankyou.html')

    return render(request, 'facades/contact.html', {'form': form})
#----------------------------------------------------------------------------------------------
