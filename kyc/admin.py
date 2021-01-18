from django.contrib import admin
from . models import KycModel

# Register your models here.
class KycAdmin(admin.ModelAdmin):
    list_display = ['__str__','owner','kyc_approve']
    class Meta:
        model = KycModel

admin.site.register(KycModel,KycAdmin)