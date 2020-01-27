from django.contrib import admin
from .models import LoanApplication, RequestHeaderModel, BusinessModel, AddressModel, HomeAddressModel, OwnersModel, SelfReportedCashFlowModel, CFApplicationDataModel

# Register your models here.
admin.site.register(LoanApplication)
admin.site.register(RequestHeaderModel)
admin.site.register(BusinessModel)
admin.site.register(AddressModel)
admin.site.register(HomeAddressModel)
admin.site.register(OwnersModel)
admin.site.register(SelfReportedCashFlowModel)
admin.site.register(CFApplicationDataModel)
