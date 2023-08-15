from django.urls import path,include
from .views import *

app_name = "facades"

urlpatterns = [
    path('',HomePage,name="home"),
    path('contact/',contact,name="contact"),
    path('CreateSurvey/',CreateSurvey,name="CreateSurvey"),
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard/<int:address_id>/',dashboard,name="dashboard_id"),
    path('aboutUs/',aboutUs,name="aboutUs"),
    path('FAQ/',FAQ,name="FAQ"),
]
