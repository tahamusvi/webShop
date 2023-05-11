from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('detail/',detail,name='detail'),
    path('add/<int:product_id>/',cart_add,name='cart_add'),
    path('remove/<int:product_id>/',cart_remove,name='cart_remove'),
]
