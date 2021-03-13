from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class KycModel(models.Model):
    
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

    Wallets = (
    ('bitcoin','Bitcoin'),
    ('etherum','Ethereum'),
    ('fitoken','FIToken'),
    )

    Approved = (
    ('Approved','Approved'),
    ('Cancel','cancel'),
    )

    owner = models.ForeignKey(User,related_name='kyc_owner', on_delete=models.CASCADE,blank=True)
    first_name = models.CharField(("first_name"), max_length=50,null=True)
    last_name = models.CharField(("last_name"), max_length=50,null=True)
    age = models.IntegerField(("age"),null=True)
    gender = models.CharField(("gender"), max_length=50,choices=Gender)
    nationality = models.CharField(("nationality"), max_length=50,null=True)
    country = CountryField()
    phone_number = PhoneNumberField()
    wallet_balance = models.CharField(("wallet balance when user applied for kyc form"),blank=True, max_length=150)
    state = models.CharField(("state"), max_length=50,null=True)
    city = models.CharField(("city"), max_length=50,null=True)
    zip_code = models.CharField(("zip code"), max_length=50,null=True)
    street_address = models.CharField(("Street address"), max_length=70,null=True)
    pass_port_copy = models.ImageField(("Account Verification"), upload_to='passports', height_field=None, width_field=None, max_length=None,null=True)
    selfie_proof =models.ImageField(("profile photo"), upload_to='selfies_proof', height_field=None, width_field=None, max_length=None,null=True)
    # wallet_type = models.CharField(("wallets"), max_length=50,choices=Wallets,null=True)
    wallet_address = models.CharField(("wallet address"), max_length=50,null=True)
    card = models.CharField(("card"), max_length=50,choices=Cards,null=True)
    kyc_approve = models.CharField(("kyc approve"), max_length=50,choices=Approved,null=True,)
   


    def save(self,*args, **kwargs):
        response = "i'm updated"
        print(response)
        super(KycModel,self).save(*args, **kwargs) #it will take data and save it

    def __str__(self):
        return f'{self.owner.username} Kyc forms'

    def get_absolute_url(self):
        return reverse("kyc:submited")

