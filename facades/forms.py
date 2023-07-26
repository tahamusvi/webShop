from django import forms

class SurveyForm(forms.Form):
    name = forms.CharField(max_length=200, label='نام')
    email =  forms.EmailField(label='ایمیل')
    phone_number = forms.CharField(max_length=200, label='شماره موبایل')
    title = forms.CharField(max_length=200, label='موضوع')
    text = forms.CharField(widget=forms.Textarea, label='متن پیام')
