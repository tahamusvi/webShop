from django.db import models

# Create your models here.

class ExcelStuff(models.Model):
    file = models.FileField(upload_to='web_shop/excels/')
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.created + "-" +  self.id
