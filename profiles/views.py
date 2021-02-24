from django.shortcuts import render
from . forms import UserProfileForm
from . models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
# from shoprequests.models import ShopRequest
from django.views.generic import UpdateView
# Create your views here.

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/accounts/login/'
    refirect_field_name ='profiles:profile'
    template_name = 'profiles/profile_update.html'
    form_class = UserProfileForm
    model = UserProfile

    def get_object(self, *args, **kwargs):
        return self.request.user.userprofile
    
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['request'] = self.request
        
        return form_kwargs
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(*args, **kwargs)
        update_form = UserProfileForm(instance = self.request.user.userprofile)
        context['form']= update_form
        # try :
        #     shop = ShopRequest.objects.get(requested_user=self.request.user)
        # except ShopRequest.DoesNotExist:
        #      shop = False
        
        # print(shop,"shopiung")

        # context["shop"] = shop
        return context
    
    def form_valid(self, form):
        print("im coming from views")
        if self.request == 'POST':

            phone= form.cleaned_data['phone']
            print("im coming from views",phone)
            form.save()
        return super().form_valid(form)