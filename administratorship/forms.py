from django import forms
from .models import ExcelStuff
from facades.models import ConfigShop
#-------------------------------------
class ExcelForm(forms.ModelForm):
    file = forms.FileField(label="محل آپلود ")
    class Meta:
        model = ExcelStuff
        fields = ['file']
#-------------------------------------
class ConfigShopForm(forms.ModelForm):
    fname = forms.CharField(label="نام فروشگاه",required=False, max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ename = forms.CharField(label="نام انگلیسی فروشگاه",required=False, max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(label="لوگو",required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    black_logo = forms.ImageField(label="لوگوی مشکی",required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    phone = forms.CharField(label="تلفن",required=False, max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label="شماره تماس",required=False, max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="ایمیل",required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="توضیحات",required=False, max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    insta = forms.URLField(label="اینستاگرام",required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    whatsapp = forms.URLField(label="واتساپ",required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    telegram = forms.URLField(label="تلگرام",required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    aboutUs = forms.CharField(label="درباره ما",required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    address = forms.CharField(label="آدرس",required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    color = forms.CharField(label="رنگ",required=False, max_length=7, widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}))
    current = forms.BooleanField(label="فعالسازی",required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    home_page = forms.ChoiceField(label="صفحه اصلی",required=False, )
    news = forms.BooleanField(label="خبرها",required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    e_namad = forms.CharField(label="نماد الکترونیکی",required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    active_dargah = forms.BooleanField(label="فعال بودن درگاه",required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = ConfigShop
        fields = [
            'fname', 'ename', 'logo', 'black_logo', 'phone', 'phone_number',
            'email', 'description', 'insta', 'whatsapp', 'telegram',
            'aboutUs', 'address', 'color', 'current', 'home_page', 'news',
            'e_namad', 'active_dargah',
        ]
#-------------------------------------
class ConfigShopTextInformationForm(forms.ModelForm):
    fname = forms.CharField(label="نام فروشگاه", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ename = forms.CharField(label="نام انگلیسی فروشگاه", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="تلفن", max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label="توضیحات", max_length=200, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    phone_number = forms.CharField(label="شماره تماس", max_length=12, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="ایمیل", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    insta = forms.URLField(label="اینستاگرام", widget=forms.URLInput(attrs={'class': 'form-control'}))
    whatsapp = forms.URLField(label="واتساپ", widget=forms.URLInput(attrs={'class': 'form-control'}))
    telegram = forms.URLField(label="تلگرام", widget=forms.URLInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="آدرس", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    e_namad = forms.CharField(label="کد html ارائه شده توسط اینماد",required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    

    class Meta:
        model = ConfigShop
        fields = [
            'fname', 'ename', 'phone', 'phone_number',
            'email', 'description', 'insta', 'whatsapp', 'telegram',
            'address','e_namad'
        ]
#-------------------------------------
class ConfigShopLogoForm(forms.ModelForm):
    logo = forms.ImageField(label="لوگو", widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    black_logo = forms.ImageField(label="لوگوی مشکی", widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    

    class Meta:
        model = ConfigShop
        fields = [
            'logo', 'black_logo',
        ]
#-------------------------------------
class ConfigShopColorForm(forms.ModelForm):
    color = forms.CharField(label="رنگ", max_length=7, widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}))
    

    class Meta:
        model = ConfigShop
        fields = [
            'color', 
        ]
#-------------------------------------