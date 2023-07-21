from django.urls import path
from  .views import *

app_name = 'stuff'

urlpatterns = [
    # path('',home,name='home'),
    path('products/<slug:slug>/<slug:id>/',product_detail,name='product_detail'),
    path('showWishList/',showWishList,name='showWishList'),
    path('category/<int:id>/',Category_detail,name='category_detail'),
    path('search/', product_search, name='product_search'),
]
