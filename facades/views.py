from django.shortcuts import render,get_object_or_404
from stuff.models import Product,Category
from .models import *
from accounts.forms import *
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#----------------------------------------------------------------------------------------------
def InformationsForTemplate(request):
    Info = {}
    # Categories
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
    #forms
    formLogin = UserLoginForm
    formRegister= UserCreationForm

    #brands
    brands = Brand.objects.all()

    #shops
    shops = shop.objects.all()


    Info = {'allCategories': allCategories,'wishlistAmount':wishlistAmount,'cart':cart,'covers':covers,'form':form
    ,'formLogin':formLogin,'formRegister':formRegister,"brands":brands,"shops":shops,}

    return Info
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
    
    Info = InformationsForTemplate(request)
    Info["Categories"] = Categories
    Info["productsOfDiscount"] = discounted
    Info["products"] = news
    Info["banner"] = EndBanner.objects.all()[0]
    Info["posts"] = Post.objects.filter(is_for_landing=True)

    return render(request,'facades/landing.html',Info)
#----------------------------------------------------------------------------------------------
@login_required
def dashboard(request,address_id = None):
    profileForm = UserChangeForm(instance=request.user)
    addressForm = AddressForm()
    Info = InformationsForTemplate(request)

    if(address_id):
        address = get_object_or_404(Address,id=address_id)
        EditAddressForm = AddressForm(instance=address)
        Info["EditAddressForm"] = EditAddressForm
        Info["EditAddressId"] = address_id

    
    Info["profileForm"] = profileForm
    Info["addressForm"] = addressForm

    return render(request,'facades/dashboard.html',Info)
#----------------------------------------------------------------------------------------------
def contact(request):
    Info = InformationsForTemplate(request)

    return render(request,'facades/contact.html',Info)
#----------------------------------------------------------------------------------------------
def aboutUs(request):  
    Info = InformationsForTemplate(request)

    return render(request,'facades/aboutUs.html',Info)
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
            Info.update({'CreateSurvey':CreateSurvey})
            messages.success(request,"سوالت رو با موفقیت ارسال شد.",'background-color: rgb(0, 190, 0);')
            return render(request, 'facades/contact.html', Info)
        else:
            messages.error(request,'مشکلی تو ارسال سوالت پیش اومد.','background-color: rgb(198, 2, 2);')
            return render(request, 'facades/contact.html', Info)

    return contact(request)
#----------------------------------------------------------------------------------------------
