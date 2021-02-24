from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .forms import UserCreateForm
from django.views.generic import CreateView,TemplateView,View
from . import forms
from source import settings
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
# email 
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib import messages
from django.template import loader

# Create your views here.

class SignUp(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/signup.html'
        
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Dotescrow Account'
            html_message = loader.render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject,'message' ,fail_silently=True,html_message=html_message)
            messages.success(request, 'Please verify you email to activate you account.')
            return redirect('accounts:signup')

        return render(request, self.template_name, {'form': form})



class CoustomLoginView(LoginView):
    authentication_form = forms.CustomLoginForm

 
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            print('user is active or not ',user.is_active)
            user.save()
            print('user is active or not ',user.is_active)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('accounts:login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('accounts:signup')

