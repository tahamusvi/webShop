from django.urls import path,include
from .views import *

app_name = "blog"
urlpatterns = [    
    path('',article_list,name="home_blog"),
    path('<int:page>/',article_list,name="home_blog"),
    path('articles/<slug>/',article_detail,name="article"),
    path('authors/<int:id>/<int:page>/',author_articles,name = "author_articles"),
    path('categories/<slug>/<int:page>/',category_articles,name = "category_articles"),
    path('search/<int:page>/', article_search, name='article_search'),
]
