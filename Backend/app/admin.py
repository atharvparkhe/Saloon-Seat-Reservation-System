from django.contrib import admin
from .models import *


class SaloonModelAdmin(admin.ModelAdmin):
    list_display = ["name", "owner"]

admin.site.register(SaloonModel, SaloonModelAdmin)

class SeatsModelAdmin(admin.ModelAdmin):
    list_display = ["saloon", "seat_name", "is_available"]

admin.site.register(SeatModel, SeatsModelAdmin)


class ServicessModelAdmin(admin.ModelAdmin):
    list_display = ["saloon", "service_name", "service_cost", "service_duration"]

admin.site.register(ServiceModel, ServicessModelAdmin)