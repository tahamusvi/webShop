from django.shortcuts import render
from stuff.models import Product,Category


#----------------------------------------------------------------------------------------------
def HomePage(request):
    print("--------------------------")
    # discounted stuff
    discounted = Product.objects.filter(available=True,discounted=True)

    # New stuff in website
    news = Product.objects.filter(available=True)
    news_list = [s.id for s in news if s.is_new][0:8]
    news = news.filter(id__in=news_list)

    # Categories
    Categories = Category.objects.filter(is_sub=False)[0:4]
    allCategories = Category.objects.filter(is_sub=False)





    # return render(request,'facades/landing.html')
    return render(request,'facades/landing.html',{'products':news,'productsOfDiscount':discounted,'Categories' : Categories,'allCategories': allCategories})
#----------------------------------------------------------------------------------------------
