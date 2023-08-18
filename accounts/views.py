from sre_constants import SUCCESS
from django.shortcuts import render,redirect
from .forms import *
from  django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import *
from django.shortcuts import render,get_object_or_404
#------------------------------------------------------------------------------------------------
messages_dict = {
    "logout" : 'بعدا باز برگرد ":)',
    "login" : ' خوش اومدی رفیق.',
    "login_error" : 'رمز عبور یا شماره تلفن را اشتباه وارد کرده اید!',
    "profile" : 'با موفقیت پروفایل آپدیت شد.',
    "sign_up" : 'ثبت نام شما با موفقیت انجام شد.',
    "sign_up_error" :  'خطا در ثبت نام.',
    "add_wishlist" : 'به لیست موردعلاقه ها اضافه شد.', 
    "remove" : 'با موفقیت حذف شد.',
    "add_address" : 'آدرس با موفقیت ثبت شد.',
    "edit" : 'با موفقیت تغییر کرد.'

}

color_messages = {
    "error" : 'background-color: rgb(198, 2, 2);',
    "success" : 'background-color: rgb(0, 190, 0);',
    "gray" : 'background-color: rgb(108, 105, 105);',

}
#------------------------------------------------------------------------------------------------
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phoneNumber=cd['phoneNumber'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,messages_dict["login"],color_messages['success'])
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                else:
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,messages_dict['login_error'],color_messages['error'])

    Loginform = UserLoginForm()
    Registerform = UserCreationForm()      
    return render(request, 'accounts/login.html', {'Loginform': Loginform,'Registerform': Registerform})
#------------------------------------------------------------------------------------------------
def profile(request):
    if request.method == 'POST':
        profileForm = UserChangeForm(request.POST,instance=request.user)

        if profileForm.is_valid():
            profileForm.save()
            messages.success(request, messages_dict['profile'],color_messages['success'])
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        profileForm = UserChangeForm(instance=request.user)

    return render(request, 'facades/dashboard.html', {'profileForm': profileForm})
#------------------------------------------------------------------------------------------------
def user_logout(request):
    logout(request)
    messages.success(request,messages_dict["logout"],color_messages['gray'])
    return redirect('facades:home')
#------------------------------------------------------------------------------------------------
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, messages_dict['sign_up'], color_messages['success'])
            user = authenticate(request, username=form.cleaned_data['phoneNumber'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('facades:home')
        else:
            messages.error(request, messages_dict['sign_up_error'], color_messages['error'])
    
    Loginform = UserLoginForm()
    Registerform = UserCreationForm()
    return render(request, 'accounts/login.html', {'Loginform': Loginform,'Registerform': Registerform})
#------------------------------------------------------------------------------------------------
def AddToWish(request, id):
    if(request.user.is_authenticated):
        item = get_object_or_404(Product, id=id)

        request.user.wishlist.add(item)
        messages.success(request, messages_dict['add_wishlist'], color_messages['success'])
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("accounts:login")
#------------------------------------------------------------------------------------------------
def RomeveToWish(request, id):
    if(request.user.is_authenticated):
        item = get_object_or_404(Product, id=id)

        request.user.wishlist.remove(item)

        messages.success(request, messages_dict["remove"], color_messages['error'])
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("accounts:login")
#------------------------------------------------------------------------------------------------
def LikeComment(request, id):
    if(request.user.is_authenticated):
        comment = get_object_or_404(Comment, id=id)

        comment.likes.add(request.user)
        comment.dislikes.remove(request.user)
        
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("accounts:login")
#------------------------------------------------------------------------------------------------
def DisLikeComment(request, id):
    if(request.user.is_authenticated):
        comment = get_object_or_404(Comment, id=id)

        comment.dislikes.add(request.user)
        comment.likes.remove(request.user)
        
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("accounts:login")
#------------------------------------------------------------------------------------------------
# @login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.phone_number = request.user.phoneNumber
            address.user = request.user
            address.save()
            messages.success(request, messages_dict["add_address"],  color_messages['success'])
            return redirect('facades:dashboard')
    else:
        form = AddressForm()
    return redirect('facades:dashboard')
#------------------------------------------------------------------------------------------------
def delete_address(request,address_id):
    address = get_object_or_404(Address,id=address_id)
    address.delete()
    messages.success(request, messages_dict['remove'], color_messages['error'])
    return redirect('facades:dashboard')
#------------------------------------------------------------------------------------------------
def edit_address(request,address_id):
    address = get_object_or_404(Address,id=address_id)
    if request.method == 'POST':
        addressForms = AddressForm(request.POST,instance=address)
        if addressForms.is_valid():
            addressForms.save()
            messages.success(request, messages_dict['edit'], color_messages['gray'])
            return redirect('facades:dashboard')

    return redirect('facades:dashboard')
#------------------------------------------------------------------------------------------------