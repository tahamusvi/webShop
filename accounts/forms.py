from django import forms
from .models import User, Address
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#------------------------------------------------------------------------------------------------
class UserLoginForm(forms.Form):
    phoneNumber = forms.CharField(label="شماره تلفن",max_length=40,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'۰۹۱۲۳۴۵۶۷۸۹'}))
    password = forms.CharField(label="گذرواژه",max_length=40,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'********'}))
#------------------------------------------------------------------------------------------------
class UserCreationForm(forms.ModelForm):
    phoneNumber = forms.CharField(label="شماره تلفن", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '۰۹۱۲۳۴۵۶۷۸۹'}))
    full_name = forms.CharField(label="نام شما", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'علی صالحی'}))
    email = forms.EmailField(label="ایمیل", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AliSalehi@gmail.com'}))
    password1 = forms.CharField(label="گذرواژه", max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    password2 = forms.CharField(label="تکرار گذرواژه", max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('رمزهای عبور باید مطابقت داشته باشند.')
        return cd['password2']

    class Meta:
        model = User
        fields = ('phoneNumber', 'full_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

#------------------------------------------------------------------------------------------------
class UserChangeForm(forms.ModelForm):
    phoneNumber = forms.CharField(label="شماره تلفن", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control','readonly': True}))
    full_name = forms.CharField(label="نام شما", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'علی صالحی'}))
    email = forms.EmailField(label="ایمیل", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AliSalehi@gmail.com','readonly': True}))

    class Meta:
        model = User
        fields = ('phoneNumber', 'full_name', 'email')

#------------------------------------------------------------------------------------------------
class AddressForm(forms.ModelForm):
    postal_code = forms.CharField(label="کد پستی", max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label="آدرس", max_length=400, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="شهر", max_length=400, widget=forms.TextInput(attrs={'class': 'form-control'}))

    
    class Meta:
        model = Address
        fields = ['text', 'postal_code', 'city']
#------------------------------------------------------------------------------------------------
class ForgotPasswordForm(forms.Form):
    phoneNumber = forms.CharField(label="شماره تلفن",max_length=40,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'۰۹۱۲۳۴۵۶۷۸۹'}))
#------------------------------------------------------------------------------------------------
class CheckForm(forms.Form):
    code = forms.CharField(label="کد تایید",max_length=40,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'62440'}))
#------------------------------------------------------------------------------------------------
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label="گذرواژه جدید", max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    password2 = forms.CharField(label="تکرار گذرواژه جدید", max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
#------------------------------------------------------------------------------------------------
class ForgotPasswordWithEmailForm(forms.Form):
    email = forms.EmailField(label="ایمیل", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'AliSalehi@gmail.com'}))
#------------------------------------------------------------------------------------------------
# class CheckForm(forms.Form):
#     code = forms.CharField(label="کد تایید",max_length=40,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'62440'}))
# #------------------------------------------------------------------------------------------------
# class ChangePasswordForm(forms.Form):
#     password1 = forms.CharField(label="گذرواژه جدید", max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
#     password2 = forms.CharField(label="تکرار گذرواژه جدید", max_length=40, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
#------------------------------------------------------------------------------------------------
class CommentForm(forms.Form):
    text = forms.CharField(label="نظر شما",max_length=400,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نظرت رو اینجا میتونی وارد کنی.'}))

    rating_choices = [(str(i), str(i)) for i in range(6)]  # تعیین گزینه‌های انتخابی برای ریتینگ
    rating = forms.ChoiceField(label="امتیاز مد نظرتون رو انتخاب کنید:",choices=rating_choices,widget=forms.Select(attrs={'class':'form-control'}))

#------------------------------------------------------------------------------------------------