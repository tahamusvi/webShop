from django.urls import path
from  .views import *

app_name = 'stuff'

urlpatterns = [
    # path('',home,name='home'),
    path('products/<slug:slug>',product_detail,name='product_detail'),
    # path('category/<slug:slug>',home,name='category_filter'),
]
