from django.shortcuts import render,redirect
from kyc.models import KycModel
from kyc.forms import KycModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,TemplateView
# Create your views here.



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
        wallet_address = form.cleaned_data['wallet_address']
        # ethereum contract
        # url = f'http://93.115.29.78:5000/api/token/mainnet/address/{wallet_address}/{contract}'
        # # print('response')
        # result = requests.get(url, headers={'Authorization':'2RxsiIvEtuaPxxvP6eTs98fr55K4xJye3IqEJWhk'})
        # # print(result.json())
        # data = result.json()
        # balance = data['balance']
        # # print('got a user wallet',balance)
        # user = User.objects.get(username=self.request.user)
        # # fitoken api for usd
        # print(time,'time')
        # fit_url = f'https://api.coingecko.com/api/v3/coins/financial-investment-token/history?date={time}&localization=false'
        # fit_result = requests.get(fit_url, headers=headers)
        # fit_data = fit_result.json()
        # fit_balance = fit_data["market_data"]["current_price"]["usd"]
        # print('fit_balance',fit_balance)
        # user.current_balance = balance*fit_balance
        # print('now',user.current_balance)
        # # print('hellos',fit_result.json())
        # user.save()
        user_kyc.save()
        return super().form_valid(form)