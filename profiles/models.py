from django.contrib import auth
from django.urls import reverse
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User
from django_countries.fields import CountryField
# from phonenumber_field.modelfields import PhoneNumberField
# from src.utils import profile_unique_slug_generator
# from django.db.models.signals import pre_save
# Create your models here.
class UserProfile(models.Model):

    # personal info 
    user = models.OneToOneField(User,related_name='userprofile', on_delete=models.CASCADE)
    avatar = models.ImageField(("displays"), upload_to='displays', height_field=None, width_field=None, max_length=None,default ='default.jpeg')
    create_date = models.DateTimeField(default = timezone.now)
    Gender = (
    ('male','Male'),
    ('female','Female'),
    ('others','Others'),
    )
    Cards = (
    ('silver','Silver'),
    ('gold','Gold'),
    ('Prepaid','Prepaid'),
    )
    age = models.PositiveIntegerField(("age"),null=True,blank=True)
    first_name = models.CharField(("first name"), max_length=50,null=True,blank=True)
    last_name = models.CharField(("last name"), max_length=50,null=True,blank=True)
    username = models.CharField(("username"), max_length=50,null=True)
    gender = models.CharField(("gender"), max_length=50,choices=Gender,null=True)
    email = models.EmailField(("email"),null=True, max_length=254)
    bio = models.CharField(("About you"), max_length=250,null=True,blank=True)
    website = models.URLField(("Website"), max_length=250,null=True,blank=True)
    card = models.CharField(("card"), max_length=50,choices=Cards,null=True,blank=True)
    
    # address info 
    country = CountryField()
    street_address = models.CharField(("street address"), max_length=70,null=True,blank=True)
    city = models.CharField(("city"), max_length=50,null=True)
    state = models.CharField(("state"), max_length=50,null=True)
    zip_code = models.CharField(("zip code"), max_length=50,null=True)

    # Buying info 

    one_click_purchasing = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)



    def __str__(self):
        return f'{self.user.username} UserProfile'
    

    def save(self,*args, **kwargs):
        self.username  = self.user.username
        self.email  = self.user.email

        super(UserProfile,self).save(*args, **kwargs) #it will take data and save it
    
    # def save_again(self,*args, **kwargs):
    #     if self.username:
    #         self.username  = self.user.username
    #     if self.age:
    #         self.age = self.user.age
    #     if self.gender:
    #         self.gender  = self.user.gender
    #     if self.first_name:
    #         self.first_name  = self.user.first_name
    #     if self.last_name:
    #         self.last_name  = self.user.last_name
    #     super(UserProfile,self).save(*args, **kwargs)

        dp = Image.open(self.avatar.path) #storing avatar in varible
        if dp.height >300 or dp.width >300:
            output_size =(300,300) #set anysize you want
            dp.thumbnail(output_size) 
            dp.save(self.avatar.path) #after resing it save it in data base in place of uploaded once by user

    def get_absolute_url(self):
        return reverse("profiles:profile")

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('created userobject')
    else:
        print('not created')

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.userprofile.save()


# def userprofile_pre_save_reciever(sender,instance,*args, **kwargs):
#     if not instance.slug:
#         instance.slug = profile_unique_slug_generator(instance)
# pre_save.connect(userprofile_pre_save_reciever,UserProfile)
    