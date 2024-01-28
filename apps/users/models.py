from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('EMAIL IS REQUIRED!!')
        if not username:
            raise ValueError('USERNAME IS REQUIRED!!')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)

        return user

    """
    Function for creation of a superuser
    """

    def create_superuser(self, email, username, password):

        user = self.create_user(email=email, username=username, password=password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)

    photo = models.ImageField(blank=True, null=True, upload_to='images/')

    is_active = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    ''' Creating a string representation of the user model '''
    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
