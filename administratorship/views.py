from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserChangeForm, AddressForm
from accounts.models import Address
from facades.views import InformationsForTemplate
from .forms import *
from .models import ExcelStuff
from django.utils.text import slugify
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
                name = row[1]
                price = row[5]
                en = row[2]
                slug = slugify(row[2])
                alt = row[1]
                category_names = row[3].split(',')  # نام‌های دسته بندی را از سلول اول جدا می‌کنیم
                brand_name = row[4]
                warehouse = row[6]
                available = True if(warehouse > 0) else False
                # colors = row[7].split(',')  # رنگ‌ها را از سلول دهم جدا می‌کنیم
                short_description = "row[9]"
                description = "row[10]"
                more_info = "row[11]"
                rating = 0
                # image = row[13]

                product_barcode = row[7]

                print(row[3])
                print("--------------------")


                # ایجاد محصول جدید
                product = Product.objects.create(
                    name=name,
                    slug=slug,
                    price=price,
                    En=en,
                    image=None,
                    alt=alt,
                    available=available,
                    rating=rating,
                    warehouse=warehouse,
                    short_description=short_description,
                    description=description,
                    more_info=more_info,
                    product_barcode=product_barcode
                )
                
                # افزودن دسته بندی‌ها به محصول
                for category_name in category_names:
                    
                    category, _ = Category.objects.get_or_create(name=category_name)
                    
                    product.category.add(category)
                
                # افزودن برند به محصول
                brand, _ = Brand.objects.get_or_create(name=brand_name)
                product.brand = brand
                
                # افزودن رنگ‌ها به محصول
                # for color_name in colors:
                #     color, _ = Color.objects.get_or_create(name=color_name)
                #     product.colors.add(color)
                
                product.save()
            
            return redirect("facades:home")

    return dashboard(request)

