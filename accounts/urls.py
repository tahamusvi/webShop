from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/',user_logout, name='logout'),
    path('register/',user_register, name='register'),
    path('profile/',profile, name='profile'),
    path('forgotPassword/',forgotPassword, name='forgotPassword'),
    path('CheckCodeForgot/<slug:phoneNumber>/',CheckCodeForgot, name='CheckCodeForgot'),
    path('ChangePasswordForgot/<slug:phoneNumber>/',ChangePasswordForgot, name='ChangePasswordForgot'),   

    path('add_address/',add_address, name='add_address'),
    path('delete_address/<int:address_id>/',delete_address, name='delete_address'),
    path('edit_address/<int:address_id>/',edit_address, name='edit_address'),

    path('AddComment/<int:id>/',AddComment, name='AddComment'),

    path('AddToWish/<int:id>/',AddToWish, name='AddToWish'),
    path('RomeveToWish/<int:id>/',RomeveToWish, name='RomeveToWish'),
    path('LikeComment/<int:id>/',LikeComment, name='LikeComment'),
    path('DisLikeComment/<int:id>/',DisLikeComment, name='DisLikeComment'),
]
