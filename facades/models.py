from unittest import result
from django.db import models
from django.urls import reverse
# Create your models here.
for_what_choices = (
        ('c2' , "2col"),
        ('c3' , "3col"),
        ('f1' , "fisrt1"),
        ('f2' , "fisrt2"),
        ('b1' , "big1"),
        ('e1' , "end1"),
        ('t1',"category1"),
        ('t2',"category2"),
        ('t3',"category3"),
        ('ct',"category page"),
        ('ds',"dashboard"),
        ('ne',"news"),
        ('au',"aboutUs"),
        ('ay',"aboutUsBanner"),
        ('co',"contact"),
        ('fq',"FAQ"),
        ('ff',"full width FAQ"),
        ('to',"Track Order"),

)
home_page_choices = (
    ('a1' , "discounted_showcase"),
    ('a2' , "category_showcase"),
)
#----------------------------------------------------------------------------------------------
class ConfigShop(models.Model):
    fname = models.CharField(max_length=200)
    ename = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='media/config/logo/')
    black_logo = models.ImageField(upload_to='media/config/logo/')

    phone = models.CharField(max_length=12)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    description = models.CharField(max_length=200)

    insta = models.URLField()
    whatsapp = models.URLField()
    telegram = models.URLField()

    aboutUs = models.TextField()
    address = models.CharField(max_length=100)

    color = models.CharField(max_length=6,default="82981a")


    current = models.BooleanField(default=False)

    home_page = models.CharField(max_length=2,choices=home_page_choices,default="a1")
    news = models.BooleanField(default=True)

    




    def __str__(self):
        return f"{self.fname} - {self.ename}"
#----------------------------------------------------------------------------------------------
class Survey(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=200,default="None")
    title = models.CharField(max_length=200)
    text = models.TextField(default="None")

    def __str__(self):
        return f"{self.email} - {self.name}"
#----------------------------------------------------------------------------------------------
class FAQGroup(models.Model):
    bigTitle = models.CharField(max_length=100)

    def __str__(self):
        return self.bigTitle
#----------------------------------------------------------------------------------------------
class FAQ(models.Model):
    group = models.ForeignKey(FAQGroup,on_delete=models.CASCADE,related_name="faqs")
    question = models.CharField(max_length=100)
    answer = models.TextField()

    def __str__(self):
        return self.question
#----------------------------------------------------------------------------------------------
class shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to='media/banners/')


    def __str__(self):
        return self.name
#----------------------------------------------------------------------------------------------
class banner(models.Model):
    bigTitle = models.CharField(max_length=200)
    smallTitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/banners/%Y/%m/')
    for_what = models.CharField(max_length=2,choices=for_what_choices)
    main_link = models.CharField(max_length=200)
    out_link = models.CharField(max_length=200)
    button = models.CharField(max_length=200,null=True,blank=True)
    arg = models.CharField(max_length=200,null=True,blank=True)



    def get_absolute_url(self):
        args = []
        if(self.arg):
            args = self.arg.split(',')
        return reverse(f"{self.main_link}:{self.out_link}",args=args)

    def __str__(self):
        return self.bigTitle

    @staticmethod
    def filter():
        banners = banner.objects.all()
        result = {}

        for what in for_what_choices:
            reason = what[0]
            result[reason] = banners.filter(for_what=reason)

        return result







