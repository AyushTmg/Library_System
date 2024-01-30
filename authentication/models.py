from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom User  model that supports using email as
    USERNAME_FIELD instead of username.
    """
    fullname=models.CharField(max_length=150)
    email=models.EmailField(unique=True)

    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=CustomUserManager()


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['fullname']

    def __str__(self) -> str:
        return f"{self.fullname}"
    