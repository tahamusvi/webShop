from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from accounts.models import User
#----------------------------------------------------------------------------------------------
from django.core.paginator import Paginator
def post_list(request,page=1):
    queryset = Post.objects.published()[::-1]

    paginator = Paginator(queryset, 8)
    posts = paginator.get_page(page)


    return render(request,"blog/post_list.html",{'posts':posts})
#----------------------------------------------------------------------------------------------
from accounts.forms import CommentForm
class PostDetail(DetailView):
    template_name = "blog/Post_detail.html"
    context_object_name = "post"

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Post.objects.published(), slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CommentForm'] = CommentForm
        return context
#----------------------------------------------------------------------------------------------
# class AuthorDetail(ListView):
#     paginate_by = 3
#     template_name = "posts/classBaseViews/Author_detail.html"

#     def get_queryset(self):
#         global Author
#         phoneNumber = self.kwargs.get('phoneNumber')
#         Author = User.objects.get(phoneNumber=phoneNumber)
#         return Author.posts.published()[::-1]

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Author'] = Author
#         return context
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
