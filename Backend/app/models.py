from django.db import models
from base.models import *
from authentication.models import *

class SaloonModel(BaseModel):
    owner = models.OneToOneField(SellerModel, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to="saloon")
    address = models.TextField()
    town = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.IntegerField(default=0)
    start_timings = models.TimeField(default="09:00:00")
    end_timings = models.TimeField(default="18:00:00")
    def __str__(self):
        return self.name


class ServiceModel(BaseModel):
    saloon = models.ForeignKey(SaloonModel, related_name="saloon_services", on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50)
    service_cost = models.FloatField(default=100)
    service_duration = models.DurationField()
    def __str__(self):
        return self.service_name


class SeatModel(BaseModel):
    saloon = models.ForeignKey(SaloonModel, related_name="saloon_seats", on_delete=models.CASCADE)
    seat_name = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.seat_name
    class Meta:
        ordering = ['seat_name']


# class WorkerServices(BaseModel):
#     worker = models.ForeignKey(WorkerModel, related_name="worker_service", on_delete=models.CASCADE)
#     service_name = models.CharField(max_length=50)
#     duration = models.DurationField()
#     cost = models.FloatField()
#     def __str__(self):
#         return self.service_name