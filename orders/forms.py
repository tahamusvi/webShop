from django import forms
from .models import Order

class CouponForm(forms.Form):
    code = forms.CharField()

#-------------------------------------
class receiptForm(forms.ModelForm):
    receipt = forms.ImageField(label="محل آپلود رسید")
    class Meta:
        model = Order  
        fields = ['receipt']  
