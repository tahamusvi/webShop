from django.urls import path,include
from . import views

app_name = "facades"

urlpatterns = [
    path('',views.HomePage,name="home"),
]
