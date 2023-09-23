from django.urls import path
from .views import *


app_name = 'orders'

urlpatterns = [
    path('create/<int:address_id>/',order_create,name='order_create'),
    path('<int:order_id>/',detail, name='detail'),
    # path('apply/<int:order_id>/',coupon_apply,name='coupon_apply'),
    path('factor/<int:order_id>/',factor, name='factor'),
    
    #Zarin pal
    # path('request/<int:order_id>/<int:price>', send_request, name='request'),
    path('verify/', verify , name='verify'),
]
