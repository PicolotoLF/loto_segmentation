from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import CustomersInfoCsv, Segments, PurchaseStatus, CustomersInfoAnalysis, CustomerInfoBoundary

admin.site.register(CustomersInfoCsv)
admin.site.register(Segments)
admin.site.register(PurchaseStatus)
admin.site.register(CustomersInfoAnalysis)
admin.site.register(CustomerInfoBoundary)