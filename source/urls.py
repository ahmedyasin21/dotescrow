"""source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from . import views, settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Dashboard.as_view(),name = 'dashboard'),

    #Auth django stuff 
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name ='password_reset'),
    path('passsword_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name = 'password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name ='password_reset_complate'),
    path('logout/',auth_views.LogoutView.as_view(),name ='logout'),
    # Apps root 

    path('accounts/', include('accounts.urls',namespace = 'accounts')),
    path('profiles/', include('profiles.urls',namespace = 'profiles')),
    path('kyc/', include('kyc.urls',namespace = 'kyc')),



]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
