from django.shortcuts import render,redirect
from kyc.models import KycModel
from kyc.forms import KycModelForm
from profiles.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,TemplateView
from datetime import datetime
from django.http import HttpResponse,JsonResponse
# Create your views here.


import requests
import json
#User = CustomUser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
contract = '0xaf79C4c4106b7C35c2FeC72D130783524f821D89'
# time = datetime.now().strftime("%Y-%m-%d")
time = datetime.now().strftime("%d-%m-%Y")


def wallet_balance(request):
    wallet_address = request.GET.get('address')
    print('imi im ',wallet_address)
    url = f'http://13.127.251.36:8000/api/fit/getBalance/{wallet_address}'
                # print('response')
    result = requests.get(url)
                # print(result.json())
    data = result.json()
    balance = data['payload']['token']
    parse_balance = float(balance)
    print('got a user wallet',parse_balance)
                # fitoken api for usd
    # print(time,'time')
    # fit_url = f'https://api.coingecko.com/api/v3/coins/financial-investment-token/history?date={time}&localization=false'
    # fit_result = requests.get(fit_url, headers=headers)
    # fit_data = fit_result.json()
    # fit_balance = fit_data["market_data"]["current_price"]["usd"]
    # print('fit_balance',fit_balance)
    # print('now',parse_balance*fit_balance)
    #             # print('hellos',fit_result.json())
    # current_balance = parse_balance*fit_balance
    current_balance = parse_balance

    return JsonResponse({'error':f'Your current balance {current_balance}   (FITokens)','error1':current_balance})


class SubmitKycTemplateView(LoginRequiredMixin,TemplateView):
    login_url = '/accounts/login/'
    template_name = "kyc/kyc_detail.html"


class KycFormCreateView(LoginRequiredMixin,CreateView):
    login_url = '/accounts/login/'
    form_class = KycModelForm
    model = KycModel
    template_name = "kyc/new_kyc.html"
    
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        return form_kwargs

    def get(self,request,*args, **kwargs):
        userkyc  = KycModel.objects.filter(owner=self.request.user).count()
        print('Kyc ki tadaaat',userkyc)
        # print('user kyc form count ',userkyc.count())
        if userkyc >=1:
            return redirect('kyc:submited')
        else:
            form = self.form_class()
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        user_kyc = form.save(commit=False)
        user_kyc.owner = self.request.user
        # print(user_kyc.owner,"hogya hai")
        user = self.request.user
        # print("coming  user from kyc view",user)
        try :
            user_profile = UserProfile.objects.get(user=user)
            # print("coming from kyc view",user_profile)
        except UserProfile.DoesNotExist:
            user_profile = None
            # print("coming  user_profile from kyc view",user_profile)
        wallet_address = form.cleaned_data['wallet_address']

        age = form.cleaned_data['age']
        # print("coming age from kyc view",age)
        first_name = form.cleaned_data['first_name']
        # print("coming first_name from kyc view",first_name)
        last_name = form.cleaned_data['last_name']
        # print("coming last_name from kyc view",last_name)
        gender = form.cleaned_data['gender']
        # print("coming gender from kyc view",gender)
        country = form.cleaned_data['country']
        # print("coming country from kyc view",country)
        street_address = form.cleaned_data['street_address']
        # print("coming street_address from kyc view",street_address)
        city = form.cleaned_data['city']
        # print("coming city from kyc view",city)
        state = form.cleaned_data['state']
        # print("coming state from kyc view",state)
        zip_code = form.cleaned_data['zip_code']
        # print("coming zip_code from kyc view",zip_code)
        card = form.cleaned_data['card']
        # print("coming card from kyc view",card)


        if not user_profile.age:
            print('im im im im im view from kyc')
            user_profile.age = age
            user_profile.save()
        # print("coming user_profile.age from kyc view",user_profile.age)
        if not user_profile.first_name:
            user_profile.first_name = first_name
            user_profile.save()
        # print("coming user_profile.first_name from kyc view",user_profile.first_name)
        if not user_profile.last_name:
            user_profile.last_name = last_name
            user_profile.save()
        # print("coming user_profile.last_name from kyc view",user_profile.last_name)
        if not user_profile.country:    
            user_profile.country = country
            user_profile.save()
        # print("coming user_profile.country from kyc view",user_profile.country)
        if not user_profile.gender:
            user_profile.gender = gender
            user_profile.save()
        # print("coming user_profile.country from kyc view",user_profile.gender)
        if not user_profile.street_address:
            user_profile.street_address = street_address
            user_profile.save()
        # print("coming user_profile.street_address from kyc view",user_profile.street_address)
        if not user_profile.city:
            user_profile.city = city
            user_profile.save()
        # print("coming user_profile.city from kyc view",user_profile.city)
        if not user_profile.state:
            user_profile.state = state
            user_profile.save()
        # print("coming user_profile.state from kyc view",user_profile.state)
        if not user_profile.zip_code:
            user_profile.zip_code = zip_code
            user_profile.save()
        # print("coming user_profile.zip_code from kyc view",user_profile.zip_code)
        if not user_profile.card:
            user_profile.card = card
            # print("coming user_profile.card from kyc view",user_profile.card)
            user_profile.save()
        # print("coming user_profile.card from kyc view",user_profile.card)
        
        

        #ethereum contract
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

        current_balance = parse_balance*fit_balance
        user_kyc.wallet_balance = f'{current_balance}   (FITokens)'
        user_kyc.save()
        return super().form_valid(form)