from django.urls import path
from .views import *

app_name = "administratorship"

urlpatterns = [
    path('',dashboard,name="dashboard"),
    path('product_list/<int:id>/',check_product_list,name="check_product_list"),
    path('order/confirm/<int:id>/',order_confirmation,name="order_confirmation"),
    path('order/not_confirm/<int:id>/',order_not_confirm,name="order_not_confirm"),
    path('order/confirm_delivered/<int:id>/',order_delivered_confirm,name="order_delivered_confirm"),
    path('order/confirm_shipping/<int:id>/',order_packing_shipping_confirm,name="order_packing_shipping_confirm"),
    path('dashboard/<int:address_id>/',dashboard,name="dashboard_id"),
    path('add_group_of_product/',add_group_of_product,name="add_group_of_product"),
    path('export/',export_products_to_excel,name="export"),
]
