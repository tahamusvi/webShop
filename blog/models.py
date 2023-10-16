from django.db import models
from accounts.models import User
from .managers import CategoryManager, ArticleManager
from django.urls import reverse
from django.utils import timezone
from facades.utils import jalali_converter
from django.utils.html import format_html



class Category(models.Model):
    status_ch = (
        ('a' , "Active"),
        ('d', "Deactive"),
    )
    title = models.CharField(max_length=50,verbose_name="تیتر")
    slug = models.SlugField(max_length=40, unique = True,verbose_name="آدرس")
    Cover = models.ImageField(upload_to='web_shop/blog/categories/%Y/%m/',null=True,blank=True,verbose_name="تصویر")
    status = models.CharField(max_length=1,choices = status_ch,verbose_name="وضعیت")

    objects = CategoryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:category_articles",args=[self.slug,1])
        # return "comment"

    def count_articles(self):
        return self.articles.all().count()


    # class Meta:
    #     verbose_name = "دسته بندی"
    #     verbose_name_plural = "دسته بندی ها"
#-----------------------------------------------------------------------------------
class Article(models.Model):
    status_ch = (
        ('p' , "انتشار یافته"),
        ('d', "پیش نویس"),
        ('i', "در انتظار انتشار"),
        ('b',"برگشت داده شده"),
    )



    title = models.CharField(max_length=50,verbose_name="تیتر")
    text = models.TextField(verbose_name="متن")
    Author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="articles",verbose_name="نویسنده")
    Cover = models.ImageField(upload_to="web_shop/blog/articles/%Y/%m/",null=True,blank=True,verbose_name="تصویر")
    drafted = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ پیش نویس")
    publish = models.DateTimeField(default=timezone.now,verbose_name="تاریخ انتشار")
    update = models.DateTimeField(auto_now=True,verbose_name="تاریخ آپدیت")
    slug = models.SlugField(max_length=40, unique = True,verbose_name="آدرس")
    status = models.CharField(max_length=1,choices = status_ch,verbose_name="وضعیت")
    Category = models.ManyToManyField(Category,related_name = "articles",verbose_name="دسته بندی")
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    is_for_landing = models.BooleanField(default=False)

    objects = ArticleManager()

    # class Meta:
    #     verbose_name = "پست"
    #     verbose_name_plural = "پست ها"

    def preview(self):
        txtperview = self.text[:123] + " .... "
        return txtperview


    def get_absolute_url(self):
        return reverse("blog:article",args=[self.slug])

    def shamsi_date(self):
        return jalali_converter(self.publish)
    shamsi_date.short_description = "publish"

    def __str__(self):
        return f"{self.title} - {self.views}"

    def clean_text(self):
        return self.text.replace('\n', '<br>')

    def Cover_tags(self):
        return format_html("<img width=120 style='border-radius:5px' src='{}'>".format(self.Cover.url))

    def get_similar_articles(self):
        similar_articles = Article.objects.filter(Category__in=self.Category.all()).exclude(id=self.id)[:4]
        return similar_articles

    def get_comments(self):
        comments = self.comments.all()
        return comments

    def increase_views(self):
        self.views += 1
        self.save()

    @staticmethod
    def get_popular_articles():
        popular_articles = Article.objects.order_by('-views')[:5]
        return popular_articles
#-----------------------------------------------------------------------------------
class publicitar(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='web_shop/publicitar/%Y/%m/')
    main_link = models.CharField(max_length=200)
    out_link = models.CharField(max_length=200)
    arg = models.CharField(max_length=200,null=True,blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"{self.main_link}:{self.out_link}",args=self.arg)

