from django.shortcuts import render,get_object_or_404
from .models import Category, Article, publicitar
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from accounts.models import User
from django.db.models import Q
from facades.views import InformationsForTemplate
#----------------------------------------------------------------------------------------------
pagination_amount = 8
#----------------------------------------------------------------------------------------------
from django.core.paginator import Paginator
def article_list(request,page=1):
    queryset = Article.objects.published()[::-1]
    paginator = Paginator(queryset, pagination_amount)
    articles = paginator.get_page(page)

    publicitar_banner = publicitar.objects.all()[::-1][0]

    Info = InformationsForTemplate(request)
    Info.update({'articles':articles,'categories':Category.objects.all(),'views_article':Article.get_popular_articles(),'paginator':paginator,'publicitar':publicitar_banner})

    return render(request,"blog/article_list.html",Info)
#----------------------------------------------------------------------------------------------
from accounts.forms import CommentForm
def article_detail(request,slug):
    article = get_object_or_404(Article.objects.published(), slug=slug)
    article.increase_views()

    Info = InformationsForTemplate(request)
    Info.update({'article':article,'CommentForm':CommentForm})

    return render(request,"blog/article_detail.html",Info)
#----------------------------------------------------------------------------------------------
def author_articles(request,id,page=1):
    author = get_object_or_404(User.objects.all(), id=id)
    
    queryset = author.articles.published()[::-1]
    paginator = Paginator(queryset, pagination_amount)
    articles = paginator.get_page(page)

    publicitar_banner = publicitar.objects.all()[::-1][0]

    Info = InformationsForTemplate(request)
    Info.update({'articles':articles,'categories':Category.objects.all(),'views_article':Article.get_popular_articles(),'paginator':paginator,'author':author,'publicitar':publicitar_banner})

    return render(request,"blog/article_list.html",Info)
#----------------------------------------------------------------------------------------------
def category_articles(request,slug,page=1):
    cat = get_object_or_404(Category.objects.all(), slug=slug)
    
    queryset = cat.articles.published()[::-1]
    paginator = Paginator(queryset, pagination_amount)
    articles = paginator.get_page(page)

    publicitar_banner = publicitar.objects.all()[::-1][0]

    Info = InformationsForTemplate(request)
    Info.update({'articles':articles,'categories':Category.objects.all(),'views_article':Article.get_popular_articles(),'paginator':paginator,'category':cat,'publicitar':publicitar_banner})

    return render(request,"blog/article_list.html",Info)
#----------------------------------------------------------------------------------------------
def article_search(request,page=1):
    query = request.GET.get('query')
    articles_list = Article.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))

    paginator = Paginator(articles_list, pagination_amount)
    articles = paginator.get_page(page)

    publicitar_banner = publicitar.objects.all()[::-1][0]

    Info = InformationsForTemplate(request)
    Info.update({'articles':articles,'categories':Category.objects.all(),'views_article':Article.get_popular_articles(),'paginator':paginator,'query':query,'publicitar':publicitar_banner})

    return render(request,"blog/article_list.html",Info)
#----------------------------------------------------------------------------------------------
