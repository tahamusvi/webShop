from django.urls import path
from .views import *

app_name = "administratorship"

urlpatterns = [
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard/<int:address_id>/',dashboard,name="dashboard_id"),
    path('add_group_of_product/',add_group_of_product,name="add_group_of_product"),
]
