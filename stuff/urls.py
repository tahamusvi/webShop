from django.urls import path
from  .views import *

app_name = 'stuff'

urlpatterns = [
    # path('',home,name='home'),
    path('products/<slug:slug>/<slug:id>/',product_detail,name='product_detail'),
    path('showWishList/<int:page>/',showWishList,name='showWishList'),
    path('category/<int:id>/<int:page>/',Category_detail,name='category_detail'),
    path('search/<int:page>/', product_search, name='product_search'),
    path('copy/', CopyObjects, name='copy'),
]
