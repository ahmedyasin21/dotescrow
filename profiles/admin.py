from django.contrib import admin
from profiles.models import UserProfile
# Register your models here.


class NameingAdmin(admin.ModelAdmin):
    list_display = ['__str__','user']
    class Meta:
        model = UserProfile

admin.site.register(UserProfile,NameingAdmin)