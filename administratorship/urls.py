from django.urls import path
from .views import *

app_name = "administratorship"

urlpatterns = [
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard/<int:address_id>/',dashboard,name="dashboard_id"),
]
