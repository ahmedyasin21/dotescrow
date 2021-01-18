from django.conf.urls import url
from django.urls import path
from accounts import views



app_name = 'accounts'

urlpatterns = [
    path('login/',views.CoustomLoginView.as_view(template_name='accounts/login.html'),name = 'login'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    path('activate/<uidb64>/<token>/',views.ActivateAccount.as_view(), name='activate'),
]
