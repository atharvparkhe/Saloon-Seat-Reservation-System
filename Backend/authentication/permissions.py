from rest_framework.permissions import BasePermission
from .models import *


class SellerPermission(BasePermission):
    message = "Only a Seller can do this"
    def has_permission(self, request, view):
        if SellerModel.objects.filter(email=request.user.email).exists():
            return True
        return False


# class WorkerPermission(BasePermission):
#     message = "Only a Worker can do this"
#     def has_permission(self, request, view):
#         if WorkerModel.objects.filter(email=request.user.email).exists():
#             return True
#         return False