from django.urls import reverse
from django.db import models
from django.contrib import auth
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.

class User(auth.models.User,auth.models.PermissionsMixin):
    
    def __str__(self):
        return "@{}".format(self.username)

