from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from kyc import views



app_name = 'kyc'

urlpatterns = [
    path('kyc_form/', views.SubmitKycTemplateView.as_view(),name = 'submited'),
    path('kyc',views.KycFormCreateView.as_view(),name='kyc_form'),
]
