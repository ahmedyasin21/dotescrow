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

    Address_proof= (
    ('1','Licence'),
    ('2','Government id'),
    ('3','Passport'),
    )

    Approved = (
    ('Approved','Approved'),
    ('Cancel','cancel'),
    )

    Varification = (
    ('1','ID Card'),
    ('2','Passport'),
    )

    owner = models.ForeignKey(User,related_name='kyc_owner', on_delete=models.CASCADE,blank=True)
    first_name = models.CharField(("first name"), max_length=50,null=True)
    last_name = models.CharField(("last name"), max_length=50,null=True)
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
    verification_field = models.CharField(("Varification"), max_length=50,choices=Varification,null=True)
    pass_port_copy = models.ImageField(("Account Verification"), upload_to='passports', height_field=None, width_field=None, max_length=None,null=True)
    selfie_proof =models.ImageField(("ID Photo"), upload_to='selfies_proof', height_field=None, width_field=None, max_length=None,null=True)
    address_proof = models.CharField(("address proof"), max_length=50,choices=Address_proof)
    address_proof_img = models.ImageField(("Address Verification"), upload_to='address_proof_img', height_field=None, width_field=None, max_length=None)
    
    # wallet_type = models.CharField(("wallets"), max_length=50,choices=Wallets,null=True)
    wallet_address = models.CharField(("wallet address"), max_length=50,null=True)
    card = models.CharField(("card"), max_length=50,choices=Cards,null=True)
    kyc_approve = models.CharField(("kyc approve"), max_length=50,choices=Approved,null=True,blank=True)
   


    def save(self,*args, **kwargs):
        response = "i'm updated"
        print(response)
        super(KycModel,self).save(*args, **kwargs) #it will take data and save it

    def __str__(self):
        return f'{self.owner.username} Kyc forms'

    def get_absolute_url(self):
        return reverse("kyc:submited")

