from django import forms
from .models import *
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
    
    class Meta:
        model = Address
        fields = ['text', 'postal_code', 'city', 'phone_number', 'current']
