from django.urls import path,include
from .views import *

app_name = "blog"
urlpatterns = [    

    # path('',PostListView.as_view(),name="home"),
    # path('<int:page>/',PostListView.as_view(),name = "home"),
    path('posts/<slug>/',PostDetail.as_view(),name = "post"),
    # path('Authors/<slug:phoneNumber>',AuthorDetail.as_view(),name = "author"),
    # path('Authors/<slug:phoneNumber>/<int:page>',AuthorDetail.as_view(),name = "author"),
    # path('Category/<slug>',CategoryDetail.as_view(),name = "category"),
    # path('Category/<slug>/<int:page>',CategoryDetail.as_view(),name = "category"),
]
