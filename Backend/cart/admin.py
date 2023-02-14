from django.contrib import admin
from .models import *

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["owner", "is_completed"]
    # list_display = ["owner", "is_completed", "total_price", "coupon_applied"]

admin.site.register(OrderModel, OrderModelAdmin)


# class OrderItemsModelAdmin(admin.ModelAdmin):
#     list_display = ["service", "seats"]

# admin.site.register(OrderItemModel, OrderItemsModelAdmin)