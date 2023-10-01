from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import random
#-----------------------------------------------------------------------------------
class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    logo = models.ImageField(upload_to='web_shop/logos/')
    description = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('stuff:product_detail',args=[self.slug,self.id])
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
        return reverse('stuff:category_detail',args=[self.id,1])
#-----------------------------------------------------------------------------------        
class Color(models.Model):
    name = models.CharField(max_length=50)
    en = models.CharField(max_length=50)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.name
#-----------------------------------------------------------------------------------
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products')
    brand = models.ForeignKey(Brand,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    
    price = models.IntegerField()
    image = models.ImageField(upload_to='web_shop/products/%Y/%m/')
    alt = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    colors = models.ManyToManyField(Color)
    warehouse = models.IntegerField(default=0)

    short_description = models.TextField()
    description = models.TextField()
    more_info = models.TextField()



    discount = models.IntegerField(default=0)
    discounted = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('stuff:product_detail',args=[self.slug,self.id])

    @property
    def discounted_price(self):
        show = int(((self.price)*(100-self.discount))/100)
        formatted_price = "{:,.0f}".format(show)
        return formatted_price
        
    @property
    def discounted_price_int(self):
        show = int(((self.price)*(100-self.discount))/100)
        return show
    
    def get_comments(self):
        comments = self.comments.all().filter(valid=True)
        return comments

    @property
    def is_new(self):
        return True if(timezone.now().day - self.updated.day <= 4) else False

    def change_available(self,quantity):
        self.warehouse -= quantity
        self.available = True if(self.warehouse > 0) else False
        self.save()
        return 

    def __str__(self):
        return self.name

    def star_rating(self):
        return self.rating * 20


    def get_similar_products(self):
        similar_products = Product.objects.filter(category__in=self.category.all()).exclude(id=self.id)[:6]
        
        if similar_products.count() < 6:
            remaining_count = 6 - similar_products.count()
            other_products = Product.objects.exclude(category__in=self.category.all()).exclude(id=self.id)
            random_products = random.sample(list(other_products), remaining_count)
            similar_products = list(similar_products) + random_products
        
        return similar_products
#-----------------------------------------------------------------------------------
class ProductImage(models.Model):
    image = models.ImageField(upload_to='web_shop/products/%Y/%m/')
    is_main = models.BooleanField(default=False) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='images',null=True,blank=True)
    alt = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product} - {self.id}"

#-----------------------------------------------------------------------------------

