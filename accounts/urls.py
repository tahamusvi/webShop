from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/',user_logout, name='logout'),
    path('register/',user_register, name='register'),


    path('AddToWish/<int:id>/',AddToWish, name='AddToWish'),
    path('LikeComment/<int:id>/',LikeComment, name='LikeComment'),
    path('DisLikeComment/<int:id>/',DisLikeComment, name='DisLikeComment'),
]
