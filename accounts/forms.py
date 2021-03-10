from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login

      
class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(label='Email / Username')


    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ('Email / Username')
        self.fields['username'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = ('Password')
        self.fields['password'].label = ''

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=username).exists() :
            pass
        else:
            raise forms.ValidationError("Email / Username not register")
        return username




class UserCreateForm(UserCreationForm):

    class Meta:
        
        model = User
        fields = ["username","email","password1","password2"]
        
        widgets ={
            'email' : forms.TextInput(attrs={'class':'control-flow'}),
        
        }
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exist")
        return email
        
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ('Enter your username')
        self.fields['username'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = ('Enter your email')
        self.fields['email'].label = ''
        self.fields['password1'].widget.attrs['placeholder'] = ('Password')
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs['placeholder'] = ('Confirm Password')
        self.fields['password2'].label = ''

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None





  


