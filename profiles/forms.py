
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from profiles.models import UserProfile
from django.core.mail import send_mail
from datetime import datetime
from django.core import validators
from django.contrib import messages
from django.core.exceptions import ValidationError

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ("avatar","username","first_name","last_name","age","gender")
        # exclude = (,)
        # fields = ("avatar",)
        Gender = (
            ('one','Male'),
            ('two','Female'),
            )
            
        widgets ={
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'age' : forms.TextInput(attrs={'class':'form-control','title':'Age should be more then 18'}),
            'gender' : forms.Select(choices=Gender,attrs={'class': 'form-control'}),
            'username' : forms.TextInput(attrs={'class': 'form-control','id':'disabledInput'}),
          
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['username'].widget.attrs['readonly'] = True
        
    def clean_age(self):
        age = self.cleaned_data["age"]
        print(age,'hm here')
        if age < 18:
            print(age,'hm here')
            raise forms.ValidationError("You age should be 18 plus")
        return age
    

       
            
