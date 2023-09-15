from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import *
from django.shortcuts import render,get_object_or_404
import random
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import smtplib
from email.message import EmailMessage
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
    "edit" : 'با موفقیت تغییر کرد.',
    "forgot" : 'کد تغییر رمز با موفقیت ارسال شد.',
    "codeReject" : 'کد بازیابی اشتباه وارد شده است.', 
    "password_changed" : 'گذرواژه با موفقیت تغییر کرد.',
    "login_again" : 'لطفا با گذرواژه جدید لاگین کنید.',
    "error_password" : 'گذرواژه های وارد شده یکسان نیستند.',
    "cant_change_password" : 'گذرواژه این کاربر قابل تعویض نیست.',
    "numeric_error" : 'در گذرواژه از حروف نیز استفاده کنید.',
    "common_error" : 'این گذرواژه خیلی عمومی است.',
    "lentgh_error" : 'این گذرواژه کم تر از هشت کاراکتر دارد.',
    "add_informing" : 'به لیست موردعلاقه ها اضافه شد.', 
    "change_main_address" : 'آدرس اصلی با موفقیت تغییر کرد.',

}

color_messages = {
    "error" : 'background-color: rgb(198, 2, 2);',
    "success" : 'background-color: rgb(0, 190, 0);',
    "gray" : 'background-color: rgb(108, 105, 105);',

}
#------------------------------------------------------------------------------------------------
EMAIL_PORT_SSL = 465

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
def forgotPasswordWithPhone(request):
    if request.method == 'POST':
        ForgotProfile = ForgotPasswordForm(request.POST)

        if ForgotProfile.is_valid():
            cd = ForgotProfile.cleaned_data
            user = User.objects.get(phoneNumber=cd['phoneNumber'])
            user.code = random.randint(10000, 99999)
            user.save()
            messages.success(request, messages_dict['forgot'],color_messages['gray'])
            return redirect("accounts:CheckCodeForgot",user.phoneNumber)
    else:
        ForgotProfile = ForgotPasswordForm()

    return render(request, 'accounts/forgotPassword.html', {'Form': ForgotProfile,'btn_text':'ارسال کد بازیابی'})
#------------------------------------------------------------------------------------------------
from config.settings import shop_email,password_email
def forgotPasswordWithEmail(request):
    if request.method == 'POST':
        ForgotProfile = ForgotPasswordWithEmailForm(request.POST)

        if ForgotProfile.is_valid():
            cd = ForgotProfile.cleaned_data
            user = User.objects.get(email=cd['email'])
            user.code = random.randint(10000, 99999)
            user.save()
            
            msg = EmailMessage()
            msg['Subject'] = 'تغییر رمز عبور'
            msg['From'] = shop_email
            msg['To'] = user.email
            msg.set_content(f"کد تغییر رمز برای شما : {user.code}")

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
                server.login(shop_email,password_email)
                server.send_message(msg)


            messages.success(request, messages_dict['forgot'],color_messages['gray'])
            return redirect("accounts:CheckCodeForgot",user.phoneNumber)
    else:
        ForgotProfile = ForgotPasswordWithEmailForm()

    return render(request, 'accounts/forgotPassword.html', {'Form': ForgotProfile,'btn_text':'ارسال کد بازیابی'})
#------------------------------------------------------------------------------------------------
def CheckCodeForgot(request,phoneNumber):
    user = User.objects.get(phoneNumber=phoneNumber)
    if request.method == 'POST':
        CheckcodeForm = CheckForm(request.POST)

        if CheckcodeForm.is_valid():
            cd = CheckcodeForm.cleaned_data
            if(user.code == int(cd['code'])):
                user.can_change_password = True
                user.save()
                return redirect("accounts:ChangePasswordForgot",user.phoneNumber)
            else:
                messages.error(request, messages_dict['codeReject'],color_messages['error'])
                return redirect("accounts:forgotPassword")
            
    else:
        CheckcodeForm = CheckForm()

    return render(request, 'accounts/forgotPassword.html', {'Form': CheckcodeForm,'btn_text':'تایید کد'})

#------------------------------------------------------------------------------------------------
def ChangePasswordForgot(request,phoneNumber):
    user = User.objects.get(phoneNumber=phoneNumber)
    if request.method == 'POST':
        ChangeForm = ChangePasswordForm(request.POST)

        if ChangeForm.is_valid():
            cd = ChangeForm.cleaned_data
            try:
                validate_password(cd['password1'])
            except ValidationError as validation_error:
                for message in validation_error:
                    if('This password is too short. It must contain at least 8 characters.' == message):
                        messages.error(request, messages_dict['lentgh_error'],color_messages['error'])
                    if('This password is too common.' == message):
                        messages.error(request, messages_dict['common_error'],color_messages['error'])
                    if('This password is entirely numeric.' == message):
                        messages.error(request, messages_dict['numeric_error'],color_messages['error'])
                    
                return redirect(request.META.get('HTTP_REFERER'),phoneNumber)
                
            
            if(cd['password1'] == cd['password2']):
                if(user.can_change_password):
                    user.set_password(cd['password1'])
                    user.can_change_password = False
                    user.save()
                    messages.error(request, messages_dict['password_changed'],color_messages['success'])
                    messages.error(request, messages_dict['login_again'],color_messages['gray'])         
                    return redirect('facades:home')
                else:
                    messages.error(request, messages_dict['cant_change_password'],color_messages['error'])
                    return redirect('facades:home')
            else:
                messages.error(request, messages_dict['error_password'],color_messages['error'])
                return redirect('accounts:ChangePasswordForgot',phoneNumber)
            
    else:
        ChangeForm = ChangePasswordForm()

    return render(request, 'accounts/forgotPassword.html', {'Form': ChangeForm,'btn_text':'تغییر رمز'})
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
            cd = form.cleaned_data
            try:
                validate_password(cd['password1'])
            except ValidationError as validation_error:
                for message in validation_error:
                    if('This password is too short. It must contain at least 8 characters.' == message):
                        messages.error(request, messages_dict['lentgh_error'],color_messages['error'])
                    if('This password is too common.' == message):
                        messages.error(request, messages_dict['common_error'],color_messages['error'])
                    if('This password is entirely numeric.' == message):
                        messages.error(request, messages_dict['numeric_error'],color_messages['error'])
                    
                return redirect('accounts:login')
            
            user = form.save(commit=False)
            user.set_password(cd['password1'])
            user.save()
            messages.success(request, messages_dict['sign_up'], color_messages['success'])
            user = authenticate(request, username=cd['phoneNumber'], password=cd['password1'])
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
def AddToInforming(request, id):
    if(request.user.is_authenticated):
        item = get_object_or_404(Product, id=id)

        request.user.informing.add(item)
        messages.success(request, messages_dict['add_informing'], color_messages['success'])
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("accounts:login")
#------------------------------------------------------------------------------------------------
def AddComment(request,id,type):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():

            if(type == 0):
                item = get_object_or_404(Product, id=id)
                comment = ProductComment(user=request.user,product=item,text=form.cleaned_data['text'],rating=form.cleaned_data['rating'])
                comment.save()
            elif(type == 1):
                item = get_object_or_404(Post, id=id)
                comment = PostComment(user=request.user,post=item,text=form.cleaned_data['text'],rating=form.cleaned_data['rating'])
                comment.save()
            else:
                messages.error(request, messages_dict['sign_up_error'], color_messages['error'])
                return redirect(request.META.get('HTTP_REFERER'))


            messages.success(request,"بعد از تایید ادمین نظر شما ثبت خواهد شد", color_messages['success'])
            return redirect(request.META.get('HTTP_REFERER'))
                
        else:
            messages.error(request, messages_dict['sign_up_error'], color_messages['error'])

    return redirect(request.META.get('HTTP_REFERER'))
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
def change_main_address(request):
    if request.method == 'POST':
        address_id = request.POST["address_id"]
        address = get_object_or_404(Address,id=address_id)
        addresses = request.user.addresses.all()
        for ad in addresses:
            ad.current = False
            ad.save()
        address.current = True
        address.save()
        messages.success(request, messages_dict["change_main_address"],  color_messages['success'])
        return redirect(request.META.get('HTTP_REFERER'))
    

    return redirect(request.META.get('HTTP_REFERER'))

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