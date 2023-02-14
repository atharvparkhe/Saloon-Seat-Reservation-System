from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('make-booking/', views.makeBooking, name="seatBooking"),
    path('past-bookings/', views.UserPastOrders, name="UserPreviousOrders"),
    path('seller-update-orders/', views.sellerComplete, name="sellerComplete"),
    path('seller-orders/', views.sellerOrders, name="sellerOrders"),
]