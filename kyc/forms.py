from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core import validators
from kyc.models import KycModel
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from web3 import Web3,HTTPProvider
import web3
from datetime import datetime
from django.core import validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib import messages

import requests
import json
#User = CustomUser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
contract = '0xaf79C4c4106b7C35c2FeC72D130783524f821D89'
# time = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%d-%m-%Y")









class KycModelForm(forms.ModelForm):
    
    class Meta:
        model = KycModel
        fields = ("first_name","last_name","age","gender","nationality","country","phone_number","address_proof","address_proof_img","verification_field","wallet_balance","city","state","zip_code","street_address","pass_port_copy","selfie_proof","wallet_address","card")
        Gender = (
            ('male','Male'),
            ('female','Female'),
            ('others','Others'),
            )
            
        Cards = (
            ('silver','Silver'),
            ('gold','Gold'),
            ('diamond','Diamond'),
            )

        Wallets = (
            ('bitcoin','Bitcoin'),
            ('etherum','Ethereum'),
            ('fitoken','FIToken'),
            )


        Varification = (
            ('1','ID Card'),
            ('2','Passport'),
            )
            
        widgets ={
            'first_name' : forms.TextInput(attrs={'class':'form-control'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control'}),
            'age' : forms.TextInput(attrs={'class':'form-control'}),
            'gender' : forms.Select(choices=Gender,attrs={'class': 'form-control'}),
            'nationality' : forms.TextInput(attrs={'class':'form-control'}),
            'country': CountrySelectWidget(),
            'phone_number': PhoneNumberPrefixWidget(),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control'}),
            "user_address":forms.TextInput(attrs={'class':'form-control'}),
            'card' : forms.Select(choices=Cards,attrs={'class': 'form-control'}),
            'verification_field' : forms.Select(choices=Varification,attrs={'class': 'form-control'}),
            # 'wallet_type' : forms.Select(choices=Wallets,attrs={'class': 'form-control'}),
            "wallet_address":forms.TextInput(attrs={'class':'form-control','id':'walletaddressinput'}),
        }
        
    # def clean_age(self):
    #     age = self.cleaned_data["age"]
    #     print(age,'hm here')
    #     if age < 18:
    #         raise forms.ValidationError("You're age should be 18 plus")
    #     return age


    # def clean_wallet_address(self):
    #     wallet_address = self.cleaned_data["wallet_address"]
    #     # print(card ,'wallet_address')
    #     # print(Web3.isAddress(wallet_address),'hoja true bhai')
    #     if 42 == len(wallet_address):
    #         if not Web3.isAddress(wallet_address):
    #             raise forms.ValidationError("Please enter a valid wallet address")
    #     else:
    #         raise forms.ValidationError("Incomplete wallet address")
    #     return wallet_address

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(KycModelForm, self).__init__(*args, **kwargs)
        self.fields['card'].widget.attrs['disabled'] = True
        self.fields['wallet_address'].disabled = True
        # instance = getattr(self, 'instance', None)
        # if instance and instance.pk:
        #     self.fields['wallet_address'].disabled = True

    def clean(self):
        cleaned_data = super().clean()

        age = cleaned_data.get('age')
        wallet_balance = cleaned_data.get('wallet_balance')
        print(age)
        if age < 18:
            # raise forms.ValidationError("You're age should be 18 plus")
            age = "You're age should be 18 plus"
            self.add_error('age',age)
            raise forms.ValidationError("You're age should be 18 plus")

        card = cleaned_data.get('card')
        print(card)

        wallet_address = cleaned_data.get('wallet_address')
        print(wallet_address)
        if 42 == len(wallet_address):
            if Web3.isAddress(wallet_address):
                if not KycModel.objects.filter(wallet_address=wallet_address).exists():
                    url = f'http://13.127.251.36:8000/api/fit/getBalance/{wallet_address}'
                    # print('response')
                    result = requests.get(url)
                    # print(result.json())
                    data = result.json()
                    balance = data['payload']['token']
                    parse_balance = float(balance)
                    print('got a user wallet',parse_balance)
                    # fitoken api for usd
                    print(time,'time')
                    fit_url = f'https://api.coingecko.com/api/v3/coins/financial-investment-token/history?date={time}&localization=false'
                    fit_result = requests.get(fit_url, headers=headers)
                    fit_data = fit_result.json()
                    fit_balance = fit_data["market_data"]["current_price"]["usd"]
                    print('fit_balance',fit_balance)

                    print('now',parse_balance*fit_balance)
                    # print('hellos',fit_result.json())

                    # current_balance = parse_balance*fit_balance
                    current_balance = balance
                    # silver process
                    if card == 'silver':
                        if current_balance >= 5000:
                            pass
                        else:
                            silver_error = f'You should have at least 5000 tokens for silver card but you have{current_balance}in your wallet'
                            self.add_error('card',silver_error)
                            raise forms.ValidationError("You should have at least 5000 tokens for silver")

                    # gold process
                    elif card == 'gold':
                        if current_balance >= 10000:
                            pass
                        else:
                            golden_error = f'You should have at least 10000 tokens for gold card but you have{current_balance}in your wallet'
                            self.add_error('card',golden_error)
                            raise forms.ValidationError("You should have at least 10000 tokens for golden")
                    
                    # Prepaid process
                    elif card == 'Prepaid':
                        if current_balance >= 15000:
                            pass
                        else:
                            Prepaid_error = f'You should have at least 15000 tokens for Prepaid but you have{current_balance}in your wallet'
                            self.add_error('card',Prepaid_error)
                            raise forms.ValidationError("You should have at least 15000 tokens for diamond")
                else:
                    invalid = "Wallet address already registered"
                    self.add_error('wallet_address',invalid)
                    raise forms.ValidationError("Wallet address already registered")

            else:
                # raise forms.ValidationError("Please enter a valid wallet address")
                invalid = "Please enter a valid wallet address"
                self.add_error('wallet_address',invalid)
                raise forms.ValidationError("Please enter a valid wallet address")

        else:
            # raise forms.ValidationError("Incomplete wallet address")
            incomplete = "Incomplete wallet address"
            self.add_error('wallet_address',incomplete)
            raise forms.ValidationError("Incomplete wallet address")