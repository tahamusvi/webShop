from tkinter import PhotoImage
from turtle import title
from unicodedata import category
from django.db import models

# Create your models here.


class Cover(models.Model):
    bigTitle = models.CharField(max_length=200)
    smallTitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='web_shop/Covers/%Y/%m/%d/')


    def __str__(self):
        return self.bigTitle
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



