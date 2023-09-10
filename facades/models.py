from django.db import models
from django.urls import reverse
# Create your models here.

#----------------------------------------------------------------------------------------------
class Cover(models.Model):
    bigTitle = models.CharField(max_length=200)
    smallTitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='web_shop/Covers/%Y/%m/%d/')


    def __str__(self):
        return self.bigTitle
#----------------------------------------------------------------------------------------------
class EndBanner(models.Model):
    title = models.CharField(max_length=200)
    describe = models.CharField(max_length=200)
    image = models.ImageField(upload_to='web_shop/Covers/%Y/%m/%d/')
    button = models.CharField(max_length=200)
    main_link = models.CharField(max_length=200)
    out_link = models.CharField(max_length=200)
    arg = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"{self.main_link}:{self.out_link}",args=self.arg)
#----------------------------------------------------------------------------------------------
class Survey(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()

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
    image = models.ImageField(upload_to='web_shop/banners/')


    def __str__(self):
        return self.name




