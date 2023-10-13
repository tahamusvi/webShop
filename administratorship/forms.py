from django import forms
from .models import ExcelStuff
#-------------------------------------
class ExcelForm(forms.ModelForm):
    file = forms.FileField(label="محل آپلود ")
    class Meta:
        model = ExcelStuff
        fields = ['file']
#-------------------------------------
