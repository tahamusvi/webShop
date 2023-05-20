from django.db import models

# Create your models here.


class Cover(models.Model):
    bigTitle = models.CharField(max_length=200)
    smallTitle = models.CharField(max_length=200)
    image = models.ImageField(upload_to='web_shop/Covers/%Y/%m/%d/')


    def __str__(self):
        return self.bigTitle
