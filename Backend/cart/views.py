from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import SellerModel, CustomerModel
from authentication.permissions import SellerPermission
from .threads import send_booking_mail
from .serializers import *
from .models import *

@api_view(["POST"])
def makeBooking(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    try:
        data=request.data
        user = CustomerModel.objects.get(email = request.user.email)
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            if not ServiceModel.objects.get(id=serializer.data["service_id"]):
                return Response({"message":"Invalid Service ID"}, status=status.HTTP_404_NOT_FOUND)
            service = ServiceModel.objects.get(id=serializer.data["service_id"])
            # seats = int(serializer.data["seats"])
            timing = serializer.data["date"]
            # avialable_seats = int(saloon.saloon_seats.filter(is_available=True).count())
            # if avialable_seats < seats:
            #     return Response({"message":"These many seats are not available", "available_seats":avialable_seats}, status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
            cart_obj, _ = OrderModel.objects.get_or_create(owner=user, is_completed=False, timing=timing, service=service)
            cart_obj.save()
            # cart_item = OrderItemModel.objects.filter(order=cart_obj, service=service).first()
            # if not cart_item:
            #     OrderItemModel.objects.create(order=cart_obj, service=service, seats=seats, owner=user)
            # else:
            #     cart_item.seats += seats
            #     cart_item.save()
            # for obj in SeatModel.objects.filter(saloon=saloon, is_available=True)[:seats]:
            #     obj.is_available = False
            #     obj.save()
            thread_obj = send_booking_mail(user.email, timing, service)
            thread_obj.start()
            ser = UserOrderSerializer(cart_obj)
            return Response({"message":"Booking Done", "data":ser.data})
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def UserPastOrders(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        user = CustomerModel.objects.get(email = request.user.email)
        objs = OrderModel.objects.filter(owner=user)
        if not objs:
            return Response({"message":"Insufficient Data"}, status=status.HTTP_206_PARTIAL_CONTENT)
        serializer = UserOrderSerializer(objs, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def sellerComplete(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated, SellerPermission]
        data = request.data
        serializer = OrderUpdateSerializer(data=data)
        if serializer.is_valid():
            if not OrderModel.objects.filter(id=serializer.data["order_id"]):
                return Response({"data":serializer.data}, status=status.HTTP_404_NOT_FOUND)
            obj = OrderModel.objects.get(id=serializer.data["order_id"])
            seats = SeatModel.objects.filter(saloon=obj.saloon, is_available=False)
            if serializer.data["is_completed"] == True:
                obj.is_completed = True
                obj.save()
                return Response({"message":"Reservation for seats has been removed"}, status=status.HTTP_200_OK)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def sellerOrders(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, SellerPermission]
    try:
        user = SellerModel.objects.get(email=request.user.email)
        saloon = SaloonModel.objects.get(owner=user)
        objs = OrderModel.objects.filter(saloon=saloon).order_by("-created_at")
        if not objs:
            return Response({"message":"not enough data"}, status=status.HTTP_204_NO_CONTENT)
        serializer = OrderSerializer(objs, many=True)
        return Response({"data":serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


