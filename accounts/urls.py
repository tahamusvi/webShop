from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/',user_logout, name='logout'),
    path('register/',user_register, name='register'),
    path('check/phone/',check_phone, name='check_phone'),
    path('profile/',profile, name='profile'),

    path('forgotPassword/',forgotPasswordWithPhone, name='forgotPasswordwithPhone'),
    path('CheckCodeForgot/<slug:phoneNumber>/',CheckCodeForgot, name='CheckCodeForgot'),
    path('ChangePasswordForgot/<slug:phoneNumber>/',ChangePasswordForgot, name='ChangePasswordForgot'),

    path('forgotPasswordWithEmail/',forgotPasswordWithEmail, name='forgotPassword'),

    path('add_address/',add_address, name='add_address'),
    path('change_main_address/',change_main_address, name='change_main_address'),
    path('delete_address/<int:address_id>/',delete_address, name='delete_address'),
    path('edit_address/<int:address_id>/',edit_address, name='edit_address'),

    path('change_send_way/',change_send_way, name='change_send_way'),

    path('AddComment/<int:id>/<int:type>/',AddComment, name='AddComment'),

    path('AddToInforming/<int:id>/',AddToInforming, name='AddToInforming'),
    path('AddToWish/<int:id>/',AddToWish, name='AddToWish'),
    path('RomeveToWish/<int:id>/',RomeveToWish, name='RomeveToWish'),
    path('LikeComment/<int:id>/',LikeComment, name='LikeComment'),
    path('DisLikeComment/<int:id>/',DisLikeComment, name='DisLikeComment'),
]
