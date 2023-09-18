from django.contrib import admin
from .models import Article, Category, publicitar

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(publicitar)
