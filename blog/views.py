from django.shortcuts import render,get_object_or_404
from .models import Category, Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from accounts.models import User
from django.db.models import Q
from facades.views import InformationsForTemplate
#----------------------------------------------------------------------------------------------
pagination_amount = 1
#----------------------------------------------------------------------------------------------
from django.core.paginator import Paginator
def post_list(request,page=1):
    queryset = Post.objects.published()[::-1]
    paginator = Paginator(queryset, pagination_amount)
    posts = paginator.get_page(page)

    Info = InformationsForTemplate(request)
    Info.update({'posts':posts,'categories':Category.objects.all(),'views_post':Post.get_popular_posts(),'paginator':paginator})

    return render(request,"blog/post_list.html",Info)
#----------------------------------------------------------------------------------------------
from accounts.forms import CommentForm
def post_detail(request,slug):
    post = get_object_or_404(Post.objects.published(), slug=slug)
    post.increase_views()

    Info = InformationsForTemplate(request)
    Info.update({'post':post,'CommentForm':CommentForm})

    return render(request,"blog/Post_detail.html",Info)
#----------------------------------------------------------------------------------------------
def author_posts(request,id,page=1):
    author = get_object_or_404(User.objects.all(), id=id)
    
    queryset = author.posts.published()[::-1]
    paginator = Paginator(queryset, pagination_amount)
    posts = paginator.get_page(page)

    Info = InformationsForTemplate(request)
    Info.update({'posts':posts,'categories':Category.objects.all(),'views_post':Post.get_popular_posts(),'paginator':paginator,'author':author})

    return render(request,"blog/post_list.html",Info)
#----------------------------------------------------------------------------------------------
def category_posts(request,id,page=1):
    cat = get_object_or_404(Category.objects.all(), id=id)
    
    queryset = cat.posts.published()[::-1]
    paginator = Paginator(queryset, pagination_amount)
    posts = paginator.get_page(page)

    Info = InformationsForTemplate(request)
    Info.update({'posts':posts,'categories':Category.objects.all(),'views_post':Post.get_popular_posts(),'paginator':paginator,'author':cat})

    return render(request,"blog/post_list.html",Info)
#----------------------------------------------------------------------------------------------
def post_search(request,page):
    query = request.GET.get('query')
    posts_list = Post.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))

    paginator = Paginator(posts_list, pagination_amount)
    posts = paginator.get_page(page)

    Info = InformationsForTemplate(request)
    Info.update({'posts':posts,'categories':Category.objects.all(),'views_post':Post.get_popular_posts(),'paginator':paginator,'query':query})

    return render(request,"blog/post_list.html",Info)
#----------------------------------------------------------------------------------------------
