from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('',detail,name='detail'),
    path('checkout/',checkout,name='checkout'),
    path('add/<int:product_id>/',cart_add,name='cart_add'),
    path('remove/<slug:product_id_color>/',cart_remove,name='cart_remove'),
    path('apply/',coupon_apply,name='coupon_apply'),
]
