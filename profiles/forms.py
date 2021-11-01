
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from profiles.models import UserProfile
from django.core.mail import send_mail
from datetime import datetime
from django.core import validators
from django.contrib import messages
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
# from phonenumber_field.widgets import PhoneNumberPrefixWidget

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ("avatar","username","first_name","last_name","age","gender","country","card","email","bio","street_address","city","state","zip_code")
        # exclude = (,)
        # fields = ("avatar",)
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
                
        widgets ={
            # 'avatar': forms.ImageField(attrs={'class':'form-control'}, required=True),
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'age' : forms.TextInput(attrs={'class':'form-control','title':'Age should be more then 18'}),
            'gender' : forms.Select(choices=Gender,attrs={'class': 'form-control'}),
            'country': CountrySelectWidget(),
            # 'phone': PhoneNumberPrefixWidget(),
            'username' : forms.TextInput(attrs={'class': 'form-control','id':'disabledInput'}),
            'email' : forms.TextInput(attrs={'class': 'form-control','id':'eMail'}),
            'street_address' : forms.TextInput(attrs={'class': 'form-control','id':'Street'}),
            'city' : forms.TextInput(attrs={'class': 'form-control','id':'ciTy'}),
            'state' : forms.TextInput(attrs={'class': 'form-control','id':'sTate'}),
            'zip_code' : forms.TextInput(attrs={'class': 'form-control','id':'zIp'}),
            'bio' : forms.TextInput(attrs={'class': 'form-control','id':'bio'}),
            'card' : forms.Select(choices=Cards,attrs={'class': 'form-control'}),

            # 'website' : forms.TextInput(attrs={'class': 'form-control','id':'website'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['card'].widget.attrs['disabled'] = True
        
    def clean_age(self):
        age = self.cleaned_data["age"]
        # print(age,'hm here')
        if age is not None:
            if age < 18:
                print(age,'hm here')
                raise forms.ValidationError("You age should be 18 plus")
            return age
    
    # def clean_phone(self):
    #     phone = self.cleaned_data["phone"]
    #     print(phone,'phone i am ')
        
    

       
            
