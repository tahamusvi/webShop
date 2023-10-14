from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserChangeForm, AddressForm
from accounts.models import Address
from facades.views import InformationsForTemplate
from .forms import *
from .models import ExcelStuff
#----------------------------------------------------------------------------------------------
@login_required
def dashboard(request,address_id = None):
    profileForm = UserChangeForm(instance=request.user)
    addressForm = AddressForm()
    Info = InformationsForTemplate(request)

    if(address_id):
        address = get_object_or_404(Address,id=address_id)
        EditAddressForm = AddressForm(instance=address)
        Info["EditAddressForm"] = EditAddressForm
        Info["EditAddressId"] = address_id

    
    Info["profileForm"] = profileForm
    Info["addressForm"] = addressForm
    Info["excelForm"] = ExcelForm() 

    return render(request,'administratorship/dashboard.html',Info)
#----------------------------------------------------------------------------------------------
import openpyxl
from stuff.models import Product,Category,Brand,Color
# @csrf_exemp
def add_group_of_product(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            
            # پردازش فایل اکسل و افزودن محصولات به مدل Product
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                name = row[0]
                price = row[1]
                slug = row[2]
                alt = row[3]
                category_names = row[4].split(',')  # نام‌های دسته بندی را از سلول اول جدا می‌کنیم
                brand_name = row[5]
                available = row[6]
                colors = row[7].split(',')  # رنگ‌ها را از سلول دهم جدا می‌کنیم
                warehouse = row[8]
                short_description = row[9]
                description = row[10]
                more_info = row[11]
                rating = 0
                # image = row[13]

                # ایجاد محصول جدید
                product = Product.objects.create(
                    name=name,
                    slug=slug,
                    price=price,
                    image=None,
                    alt=alt,
                    available=available,
                    rating=rating,
                    warehouse=warehouse,
                    short_description=short_description,
                    description=description,
                    more_info=more_info
                )
                
                # افزودن دسته بندی‌ها به محصول
                for category_name in category_names:
                    category, _ = Category.objects.get_or_create(name=category_name)
                    product.category.add(category)
                
                # افزودن برند به محصول
                brand, _ = Brand.objects.get_or_create(name=brand_name)
                product.brand = brand
                
                # افزودن رنگ‌ها به محصول
                for color_name in colors:
                    color, _ = Color.objects.get_or_create(name=color_name)
                    product.colors.add(color)
                
                product.save()
            
            return redirect("facades:home")

    return dashboard(request)

