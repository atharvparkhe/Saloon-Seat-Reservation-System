from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db import models
from base.models import BaseModel
from authentication.models import *
from app.models import *


class OrderModel(BaseModel):
    owner = models.ForeignKey(CustomerModel, related_name="order_owner", on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    # total_price = models.FloatField(default=0)
    # coupon_applied = models.BooleanField(default=False)
    timing = models.DateField(auto_now=False, auto_now_add=False)
    service = models.ForeignKey(ServiceModel, related_name="booked_service", on_delete=models.CASCADE)
    def __str__(self):
        return self.owner.name


# class OrderItemModel(BaseModel):
#     saloon = models.ForeignKey(SaloonModel, related_name="saloon_orders", on_delete=models.CASCADE)
#     owner = models.ForeignKey(CustomerModel, related_name="order_item_customer", on_delete=models.CASCADE)
#     order = models.ForeignKey(OrderModel, related_name="order_items", on_delete=models.CASCADE)
#     seats = models.IntegerField(default=1)
#     total = models.FloatField(default=0)


# @receiver(pre_save, sender=OrderItemModel)
# def get_items_total(sender, instance, *args, **kwargs):
#     instance.total = instance.service.service_cost * instance.seats

# @receiver(post_save, sender=OrderItemModel)
# def get_total_amt(sender, instance, *args, **kwargs):
#     total = 0
#     cart_obj = OrderModel.objects.get(owner = instance.owner, is_completed=False)
#     for i in OrderItemModel.objects.filter(order=cart_obj):
#         total += i.total
#     cart_obj.total_price = total
#     cart_obj.save()
