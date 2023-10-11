from django.urls import path
from .views import *


app_name = 'orders'

urlpatterns = [
    path('create/<int:address_id>/',order_create,name='order_create'),
    path('create_receipt/<int:address_id>/',order_create_receipt,name='order_create_receipt'),
    # path('submit_receipt/<int:address_id>/',submit_receipt, name='submit_receipt'),
    path('<int:order_id>/',detail, name='detail'),
    # path('apply/<int:order_id>/',coupon_apply,name='coupon_apply'),
    path('factor/<int:order_id>/',factor, name='factor'),
    
    #Zarin pal
    # path('request/<int:order_id>/<int:price>', send_request, name='request'),
    path('verify/', verify , name='verify'),
]
