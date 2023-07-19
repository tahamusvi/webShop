from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import *
from stuff.models import *

# ----------------------------------------------------------------------------------------------------------------------------
class User(AbstractBaseUser):
    phoneNumber = models.CharField(unique=True, max_length=11)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    code = models.IntegerField(blank=True,null=True)


    wishlist = models.ManyToManyField(Product,blank=True)



    USERNAME_FIELD = 'phoneNumber'
    objects = MyUserManager()

    def __str__(self):
        return str(self.phoneNumber) + " - " + str(self.full_name)

    # def full_name(self):
    #     return str(self.full_name) + " " + str(self.lastName)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True




    @property
    def is_staff(self):
        return self.is_admin
# ----------------------------------------------------------------------------------------------------------------------------
class comment(models.Model):
    user = models.ManyToManyField(User,related_name="comments")
    Product = models.ManyToManyField(Product,related_name="comments")
    text = models.TextField()
    created = models.DateField(auto_now_add=True)

    rating = models.IntegerField(default=0) 
    likes = models.IntegerField(default=0) 
    dislikes = models.IntegerField(default=0) 


    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')



    def __str__(self):
        return f"{self.user} - {self.Product}" 
