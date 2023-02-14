from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('saloons/', views.SaloonLC.as_view(), name="saloonL"),
    path('saloon/<sal_id>/', views.getSingleSaloon, name="saloonR"),
    path('seller-saloon-update/', views.SaloonUpdateView, name="update-saloon-details"),

    path('services/', views.ServicesLC.as_view(), name="ServicesL"),
    path("get-services/<sal_id>/", views.getServices, name="get-services"),
    path('service/<id>/', views.ServicesR.as_view(), name="ServicesR"),
    path('seller-service-update/<sid>/', views.updateServices, name="update-service-details"),
    path('seller-service-delete/<sid>/', views.deleteServices, name="delete-service-details"),

    path('seats/<sal_id>/', views.SeatLC.as_view(), name="SeatLC"),
    path('seats/<id>/', views.SeatRUD.as_view(), name="SeatRUD"),
    path('seller-seat-update/<sid>/', views.updateSeat, name="update-seat-details"),
    path('seller-seat-delete/<sid>/', views.deleteSeat, name="delete-seat-details"),
]