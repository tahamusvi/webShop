from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from stuff.models import Product,Category
from .models import ConfigShop, shop, banner, Survey, FAQGroup
from stuff.models import Brand
from blog.models import Article
from cart.cart import Cart
from accounts.views import color_messages
from accounts.forms import UserLoginForm,UserCreationForm, UserChangeForm, AddressForm
from django.http import HttpResponseRedirect
from django.urls import reverse
#------------------------------------------------------------------------------------------------
messages_dict = {
    "send_success" : "سوالت رو با موفقیت ارسال شد.",
    "problem_in_send" : 'مشکلی تو ارسال سوالت پیش اومد.',
}
#----------------------------------------------------------------------------------------------
def InformationsForTemplate(request):
    Info = {}
    # Categories
    allCategories = Category.objects.filter(is_sub=False)[:7]
    #wishlist
    wishlistAmount = 0
    if(request.user.is_authenticated):
        wishlistAmount = request.user.wishlist.all().count()
    #forms
    form = UserLoginForm
    #cart
    cart = Cart(request)
    CartAmount = cart.get_count()
    #forms
    Loginform = UserLoginForm
    Registerform= UserCreationForm

    #brands
    brands = Brand.objects.all()

    #shops
    shops = shop.objects.all()

    site = ConfigShop.objects.get(current=True)


    Info = {'allCategories': allCategories,'wishlistAmount':wishlistAmount,'cart':cart,'form':form
    ,'Loginform':Loginform,'Registerform':Registerform,"brands":brands,"shops":shops,'site':site}
    Info["banners"] = banner.filter()
    Info["footer_articles"] = Article.objects.all()[::-1][0:3]

    return Info
#----------------------------------------------------------------------------------------------
from orders.models import Order
import requests
import json
messages_dict = {
    "not_order" : 'جنین سفارشی در دیتابیس وجود ندارد.',
    "not_connected" : ' اتصال به درگاه ناموفق بود. لطفا از پرداخت کارت به کارت استفاده نمایید.',
    "too_long" : 'زمان بیش حد سپری شده برای اتصال به درگاه.',
    "not_success_connect" : 'اتصال ناموفق.',
    "success" : 'خرید با موفقیت انجام شد.',
    "payed" : 'پرداخت انجام شده بوده است.',
    "not_success_connect" : 'پرداخت ناموفق بود.',
    "not_upload" : 'آپلود با مشکل مواجه شد.',
    "success_upload" : "آپلود با موفقیت انجام شد. برای پیگیری سفارش به داشبورد مراجعه کنید.",
}
merchant2 = "03e8b-e1775-76e11-362e1-7b4f39c1867976ae3974c0170c2e"
test_merhant = "adxcv-zzadq-polkjsad-opp13opoz-1sdf455aadzmck1244567"
CallbackURL = 'https://vahdat-sh.ir/orders/verify/'
gateway_send= 'https://bitpay.ir/payment/gateway-send'
email = 'email@example.com'  # Optional
description = "گیزموشاپ"  # Required
#----------------------------------------------------------------------------------------------
def Bitpay(request):
    print("here wait for bitpay")
    user = request.user

    try:
        user_order = Order.objects.get(id=user.order_id)
    except Order.DoesNotExist:
        messages.success(request,messages_dict['not_order'],color_messages['error'])
        return redirect('facades:home')

    amount = user_order.total_price() * 10


    data = {}
    data['api'] = merchant2
    data['redirect'] = CallbackURL
    data['amount'] = amount

    data['factorId'] = user.order_id
    data['name'] = user_order.user.full_name
    data['email'] = email
    data['description'] = description
    # response = requests.post(gateway_send, data)

    
    

    try:
        response = requests.post(gateway_send, data)
        response_dict2 = response.json()
        id_get = response.text
        print(f"response: {id_get}")



        if(int(id_get) > 0):
            user.redirect = True
            user.save()
            user.redirect_url = f"https://bitpay.ir/payment/gateway-{id_get}-get"

            return
        else:
            user.redirect = False
            user.save()
            user.redirect_url = "false"
            user_order.delete()
            messages.success(request,messages_dict['not_connected'],color_messages['error'])
            return redirect('cart:detail')


    
    except requests.exceptions.Timeout:
        messages.success(request,messages_dict['too_long'],color_messages['error'])
        return redirect('cart:detail')
    except requests.exceptions.ConnectionError:
        messages.success(request,messages_dict['not_success_connect'],color_messages['error'])
        return redirect('cart:detail')
#----------------------------------------------------------------------------------------------
from .models import home_page_choices
def HomePage(request):

    if(request.user.is_authenticated):
        user = request.user
        if(user.redirect):
            Bitpay(request)

        if(user.redirect):
            user.redirect = False
            user.save()
            return HttpResponseRedirect(user.redirect_url)
    # discounted stuff
    discounted = Product.objects.filter(available=True,discounted=True)[::-1][0:6]
    # New stuff in website
    news = Product.objects.filter(available=True)
    news_list = [s.id for s in news if s.is_new][0:8]
    news = news.filter(id__in=news_list)
    
    
    Info = InformationsForTemplate(request)
    Info["productsOfDiscount"] = discounted
    Info["products"] = news
    Info["articles"] = Article.objects.filter(is_for_landing=True)[0:3]
    if request.user.is_authenticated:
        Info["watched"] = request.user.wacthed.all().order_by('timestamp')[::-1][0:4]
    
    Info["categories"] = Category.objects.all()


    return render(request,f"facades/{dict(home_page_choices)[Info['site'].home_page]}.html",Info)
#----------------------------------------------------------------------------------------------
def contact(request):
    Info = InformationsForTemplate(request)

    return render(request,'facades/contact.html',Info)
#----------------------------------------------------------------------------------------------
def aboutUs(request):  
    Info = InformationsForTemplate(request)

    return render(request,'facades/aboutUs.html',Info)
#----------------------------------------------------------------------------------------------
from .models import Rule
def rules(request):  
    Info = InformationsForTemplate(request)
    rules = Rule.objects.all()
    Info['rules'] = rules
    return render(request,'facades/rules.html',Info)
#----------------------------------------------------------------------------------------------
def FAQ(request):
    FAQG = FAQGroup.objects.all()
    Info = InformationsForTemplate(request)
    Info["FAQG"] = FAQG

    return render(request,'facades/FAQ.html',Info)
#----------------------------------------------------------------------------------------------
from django.core.mail import send_mail
from .forms import SurveyForm

def CreateSurvey(request):
    CreateSurvey = False
    form = SurveyForm()
    Info = InformationsForTemplate(request)
    Info.update({'form': form,'CreateSurvey':CreateSurvey})

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            
            text = form.cleaned_data['text']
            title = form.cleaned_data['title']

            surveyUser = Survey(
                name = name,
                email = email,
                phoneNumber = phone_number,
                title = title,
                text = text)
            surveyUser.save()

            CreateSurvey = True
            Info.update({'CreateSurvey':CreateSurvey})
            messages.success(request,messages_dict['send_success'],color_messages['success'])
            return render(request, 'facades/contact.html', Info)
        else:
            messages.error(request,messages_dict['problem_in_send'],color_messages['error'])
            return render(request, 'facades/contact.html', Info)

    return contact(request)
#----------------------------------------------------------------------------------------------
def handler404(request, exception):
    Info = InformationsForTemplate(request)
    return render(request, 'facades/404.html', context=Info,status=404)
#----------------------------------------------------------------------------------------------