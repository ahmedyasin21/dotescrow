from django.conf.urls import url
from django.urls import path
from profiles import views



app_name = 'profiles'

urlpatterns = [
    path('profile',views.ProfileUpdateView.as_view(),name='profile')
]
