from django.contrib import admin
from .models import Doctor, ConsultDetails, Consultation
# Register your models here.

admin.site.register(Doctor)
admin.site.register(ConsultDetails)
admin.site.register(Consultation)
