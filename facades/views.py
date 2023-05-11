from django.shortcuts import render
from stuff.models import Product


#----------------------------------------------------------------------------------------------
def HomePage(request):
    print("--------------------------")
    products2 = Product.objects.filter(available=True)
    products = Product.objects.filter(available=True)

    # return render(request,'facades/landing.html')
    return render(request,'facades/landing.html',{'products':products,'productsOfDiscount':products2,})
#----------------------------------------------------------------------------------------------
