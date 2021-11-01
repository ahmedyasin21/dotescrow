
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,TemplateView
from kyc.models import KycModel


class Dashboard(LoginRequiredMixin,TemplateView):
    login_url = '/accounts/login/'
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try :
            kyc = KycModel.objects.get(owner=self.request.user)
        except KycModel.DoesNotExist:
             kyc = False
        print(kyc,"kyc")
        context["kyc"] = kyc
        return context
    

