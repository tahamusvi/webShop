from django.contrib import admin
from .models import Post, Category, publicitar

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(publicitar)
