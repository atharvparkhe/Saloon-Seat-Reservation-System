from django.contrib import admin
from .models import *

admin.site.register(CustomerModel)
# admin.site.register(CustomerAddress)

class ModelAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "is_verified"]

admin.site.register(SellerModel, ModelAdmin)

# admin.site.register(WorkerModel, ModelAdmin)