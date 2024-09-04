from unicodedata import category
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from django.utils.text import slugify
#-----------------------------------------------------------------------------------
class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True)
    logo = models.ImageField(upload_to='media/logos/')
    description = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ","-")
        super(Brand, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('stuff:product_detail',args=[self.slug,self.id])
#-----------------------------------------------------------------------------------
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='scategory',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('stuff:category_detail',args=[self.id,1])

    def save(self, *args, **kwargs):
        self.slug = self.name.replace(" ","-")
        super(Category, self).save(*args, **kwargs)
#-----------------------------------------------------------------------------------        
class Color(models.Model):
    name = models.CharField(max_length=50)
    en = models.CharField(max_length=50)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.name
#-----------------------------------------------------------------------------------
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='products',blank=True)
    brand = models.ForeignKey(Brand,related_name='products',null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    En = models.CharField(max_length=200,blank=True,null=True) 
    slug = models.SlugField(max_length=200,unique=True, allow_unicode=True)
    
    price = models.IntegerField()
    image = models.ImageField(upload_to='media/products/%Y/%m/')
    alt = models.CharField(max_length=200)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    colors = models.ManyToManyField(Color,blank=True)
    warehouse = models.IntegerField(default=0)

    short_description = models.TextField()
    description = models.TextField()
    more_info = models.TextField()

    ordered = models.IntegerField(default=0)


    product_barcode = models.IntegerField(blank=True,null=True)

    dirham_price = models.IntegerField(blank=True,null=True,default=17000) 
    dirham_rate = models.IntegerField(blank=True,null=True) 

    transit_price = models.IntegerField(blank=True,null=True,default=100000)


    discount = models.IntegerField(default=0)
    discounted = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return reverse('stuff:product_detail',args=[self.slug,self.id])

    def get_categories(self):
        categories = self.category.all()
        return "-".join([str(category) for category in categories])


    @property
    def discounted_price(self):
        show = int(((self.price)*(100+self.discount))/100)
        formatted_price = "{:,.0f}".format(show)
        return formatted_price

    @property
    def discounted_price_int(self):
        show = int(((self.price)*(100+self.discount))/100)
        return show

    @property
    def price_for_order_item(self):
        return self.discounted_price_int + self.transit_price
    
    def get_comments(self):
        comments = self.comments.all().filter(valid=True)
        return comments

    def ordered_increase(self,amount):
        self.ordered += 1
        return True

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

    def clean_short_description(self):
        return self.short_description.replace('\n', '<br>')

    def clean_description(self):
        return self.description.replace('\n', '<br>')
    
    def clean_more_info(self):
        return self.more_info.replace('\n', '<br>')

    def get_similar_products(self):
        product_ids = []
        for category in self.category.all():
            product_ids.extend(category.products.filter(available=True).exclude(id=self.id).values_list('id', flat=True)[:6])

        # remain = 6 - len(product_ids)
        # while(remain > 0):
        #     product_ids.extend(Product.objects.filter(available=True).exclude(id=self.id).values_list('id', flat=True))
        #     product_ids = list(set(product_ids))
        #     remain = 6 - len(product_ids)

        product_ids = product_ids[:6]

        similar_products = Product.objects.filter(id__in=product_ids).distinct()

        return similar_products
#-----------------------------------------------------------------------------------
class ProductImage(models.Model):
    image = models.ImageField(upload_to='media/products/%Y/%m/')
    is_main = models.BooleanField(default=False) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='images',null=True,blank=True)
    alt = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.product} - {self.id}"

#-----------------------------------------------------------------------------------

