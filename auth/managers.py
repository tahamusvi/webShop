from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self,phoneNumber,password):
        if not phoneNumber:
            raise ValueError('users must have Phone')

        user = self.model(phoneNumber=phoneNumber)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phoneNumber,password):
        user = self.create_user(phoneNumber,password)
        user.is_admin = True
        user.save(using=self._db)
        return user