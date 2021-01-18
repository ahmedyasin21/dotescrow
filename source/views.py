
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,TemplateView

class Dashboard(LoginRequiredMixin,TemplateView):
    login_url = '/accounts/login/'
    template_name = "dashboard.html"

