from django.db import models
from django.contrib.auth.models import AbstractUser
import random



class User(AbstractUser):
    id=models.IntegerField(unique=True,primary_key=True)
    first_name=models.CharField(max_length=120)
    last_name=models.CharField(max_length=120)
    email=models.EmailField(unique=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']
    
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = random.randint(10000000, 99999999) 
        super().save(*args, **kwargs)
    
    

    
