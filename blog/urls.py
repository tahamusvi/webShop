from django.urls import path,include
from .views import *

app_name = "blog"
urlpatterns = [    
    path('',post_list,name="home_blog"),
    path('<int:page>/',post_list,name="home_blog"),
    path('posts/<slug>/',post_detail,name="post"),
    path('authors/<int:id>/<int:page>/',author_posts,name = "author_posts"),
    path('categories/<slug>/<int:page>/',category_posts,name = "category_posts"),
    path('search/<int:page>/', post_search, name='post_search'),
]
