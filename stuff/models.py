from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
#-----------------------------------------------------------------------------------
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='scategory',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_filter',args=[self.slug,])
#-----------------------------------------------------------------------------------
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    image = models.ImageField(upload_to='web_shop/products/%Y/%m/%d/')
    image2 = models.ImageField(upload_to='web_shop/products/%Y/%m/%d/')
    image3 = models.ImageField(upload_to='web_shop/products/%Y/%m/%d/')
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    discount = models.IntegerField(null=True,blank=True)
    discounted = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('stuff:product_detail',args=[self.slug,self.id])

    @property
    def discounted_price(self):
        return int(((self.price)*(100-self.discount))/100)


    @property
    def is_new(self):
        return True if(timezone.now().day - self.updated.day <= 15) else False


    def __str__(self):
        return self.name
