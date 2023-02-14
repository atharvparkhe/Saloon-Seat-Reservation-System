from django.db import models
from base.models import *


class CustomerModel(BaseUser):
    token = models.CharField(max_length=50)
    def __str__(self):
        return self.email


class SellerModel(BaseUser):
    token = models.CharField(max_length=50)
    otp = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    gst_number = models.IntegerField(unique=True)
    def save(self, *args, **kwargs):
        self.is_seller = True
        super(SellerModel, self).save(*args, **kwargs) 
    def __str__(self):
        return self.email


# class WorkerModel(BaseUser):
#     profile_img = models.ImageField(upload_to="worker")
#     is_free = models.BooleanField(default=False)
#     is_verified = models.BooleanField(default=False)
#     start_timings = models.TimeField()
#     end_timings = models.TimeField()
#     def __str__(self):
#         return self.email


# class CustomerAddress(BaseModel):
#     customer = models.ForeignKey(CustomerModel, related_name="customer_address", on_delete=models.CASCADE)
#     latitude = models.IntegerField(null=True, blank=True)
#     longitude = models.IntegerField(null=True, blank=True)
#     address = models.TextField()
#     pincode = models.CharField(max_length=100)
#     town = models.CharField(max_length=50)
#     landmark = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     country = models.CharField(max_length=50, default="India")
#     def __str__(self):
#         return self.customer.email