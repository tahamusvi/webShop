from django.shortcuts import render,get_object_or_404
from .models import Category, Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from accounts.models import User
#----------------------------------------------------------------------------------------------
from django.core.paginator import Paginator
def post_list(request,page=1):
    queryset = Post.objects.published()[::-1]
    paginator = Paginator(queryset, 1)
    posts = paginator.get_page(page)

    return render(request,"blog/post_list.html",{'posts':posts,'categories':Category.objects.all(),'views_post':Post.get_popular_posts(),'paginator':paginator})
#----------------------------------------------------------------------------------------------
from accounts.forms import CommentForm
def post_detail(request,slug):
    post = get_object_or_404(Post.objects.published(), slug=slug)
    post.increase_views()
    return render(request,"blog/Post_detail.html",{'post':post,'CommentForm':CommentForm})
#----------------------------------------------------------------------------------------------
def author_posts(request,id,page=1):
    author = get_object_or_404(User.objects.all(), id=id)
    
    queryset = author.posts.published()[::-1]
    paginator = Paginator(queryset, 1)
    posts = paginator.get_page(page)

    return render(request,"blog/post_list.html",{'posts':posts,'categories':Category.objects.all(),'views_post':Post.get_popular_posts(),'paginator':paginator,'author':author})
#----------------------------------------------------------------------------------------------
def category_posts(request,id,page=1):
    cat = get_object_or_404(Category.objects.all(), id=id)
    
    queryset = cat.posts.published()[::-1]
    paginator = Paginator(queryset, 3)
    posts = paginator.get_page(page)

    return render(request,"blog/post_list.html",{'posts':posts,'categories':Category.objects.all(),'views_post':Post.get_popular_posts(),'paginator':paginator,'author':cat})
#----------------------------------------------------------------------------------------------
# class CategoryDetail(ListView):
#     paginate_by = 4
#     template_name = "posts/classBaseViews/Category_detail.html"

#     def get_queryset(self):
#         global Category
#         slug = self.kwargs.get('slug')
#         Category = get_object_or_404(models.Category.objects.actived(), slug=slug)
#         return Category.posts.published()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Category'] = Category
#         return context
#----------------------------------------------------------------------------------------------
