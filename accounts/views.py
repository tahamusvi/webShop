from django.shortcuts import render,redirect
from .forms import *
from  django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import User
from django.shortcuts import render,get_object_or_404
#------------------------------------------------------------------------------------------------
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,phoneNumber=cd['phoneNumber'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in successfully','success')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,'username or password is wrong','alert')
    else:
        form = UserLoginForm
    return redirect(request.META.get('HTTP_REFERER'))


#------------------------------------------------------------------------------------------------
def user_logout(request):
    logout(request)
    messages.success(request,'you logged out successfully','success')
    # return redirect('shop:home')


#------------------------------------------------------------------------------------------------
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['phoneNumber'],cd['full_name'],cd['password'])
            user.save()
            messages.success(request,'you registered successfully','success')
            return redirect('shop:home')
        else:
            messages.error(request,'something is wrong','alert')
    else:
        form = UserRegistrationForm
    return render(request,'accounts/register.html',{'form':form})
#------------------------------------------------------------------------------------------------
def AddToWish(request, id):
    item = get_object_or_404(Product, id=id)

    request.user.wishlist.add(item)

    # return redirect('stuff:product_detail',item.slug,item.id)
    return redirect(request.META.get('HTTP_REFERER'))
