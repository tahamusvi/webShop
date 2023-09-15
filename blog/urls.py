from django.urls import path,include
from .views import *

app_name = "blog"
urlpatterns = [    
    path('',post_list,name="home"),
    path('<int:page>/',post_list,name="home"),
    path('posts/<slug>/',post_detail,name="post"),
    path('Authors/<int:page>/<int:id>/',author_posts,name = "author_posts"),
    # path('Authors/<slug:phoneNumber>/<int:page>',AuthorDetail.as_view(),name = "author"),
    path('Category/<int:page>/<int:id>/',category_posts,name = "category"),
    # path('Category/<slug>/<int:page>',CategoryDetail.as_view(),name = "category"),
]
