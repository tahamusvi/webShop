from django.shortcuts import render,redirect
from .forms import *
from  django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import *
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
    return redirect('facades:home')
#------------------------------------------------------------------------------------------------
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد.', 'success')
            user = authenticate(request, username=form.cleaned_data['phoneNumber'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('facades:home')
        else:
            messages.error(request, 'خطا در ثبت نام.', 'alert')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
#------------------------------------------------------------------------------------------------
def AddToWish(request, id):
    if(request.user.is_authenticated):
        item = get_object_or_404(Product, id=id)

        request.user.wishlist.add(item)

        # return redirect('stuff:product_detail',item.slug,item.id)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("accounts:login")
#------------------------------------------------------------------------------------------------
def RomeveToWish(request, id):
    if(request.user.is_authenticated):
        item = get_object_or_404(Product, id=id)

        request.user.wishlist.remove(item)

        # return redirect('stuff:product_detail',item.slug,item.id)
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
            address.user = request.user
            address.save()
            return redirect('facades:dashboard')
    else:
        form = AddressForm()
    return render(request, 'accounts/add_address.html', {'form': form})
#------------------------------------------------------------------------------------------------