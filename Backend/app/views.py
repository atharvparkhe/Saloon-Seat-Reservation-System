from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import SellerModel
from authentication.permissions import SellerPermission
from .models import *
from .serializers import *

class SaloonLC(ListCreateAPIView):
    queryset = SaloonModel.objects.all()
    serializer_class = MultiSaloonSerializer
    def create(self, request):
        try:
            data = request.data
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated, SellerPermission]
            user = SellerModel.objects.get(email=request.user.email)
            serializer = SaloonGetSeriaizer(data=data)
            if serializer.is_valid():
                serializer.save(owner=user)
                return Response({"message":"Saloon added", "data":serializer.data}, status=status.HTTP_200_OK)
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class SaloonR(RetrieveAPIView):
    queryset = SaloonModel.objects.all()
    serializer_class = SaloonSerializer
    lookup_field = "id"

@api_view(["GET"])
def getSingleSaloon(request, sal_id):
    try:
        obj = SaloonModel.objects.get(id=sal_id)
        ser = SaloonSerializer(obj)
        return Response([ser.data], status=status.HTTP_200_OK)
    except Exception as e:
            return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PATCH"])
def SaloonUpdateView(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated, SellerPermission]
        user = SellerModel.objects.get(email=request.user.email)
        if not user:
            return Response({"message":"You cannot perform this"}, status=status.HTTP_401_UNAUTHORIZED)
        shop = SaloonModel.objects.get(owner=user)
        if not shop:
            return Response({"message":"Shop does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SaloonSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Saloon Details Updated", "data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ServicesLC(CreateAPIView):
    queryset = ServiceModel.objects.all()
    serializer_class = ServicesSerializer
    def create(self, request, sal_id):
        try:
            data = request.data
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated, SellerPermission]
            user = SellerModel.objects.get(email=request.user.email)
            if not user:
                return Response({"message":"You cannot perform this"}, status=status.HTTP_401_UNAUTHORIZED)
            shop = SaloonModel.objects.get(owner=user)
            if not shop:
                return Response({"message":"Shop does not exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ServicesSerializer(data=data)
            if serializer.is_valid():
                serializer.save(saloon=SaloonModel.objects.get(id=sal_id))
                return Response({"message":"Service added", "data":serializer.data}, status=status.HTTP_200_OK)
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ServicesR(RetrieveAPIView):
    queryset = ServiceModel.objects.all()
    serializer_class = ServicesSerializer
    lookup_field = "id"

@api_view(["PATCH"])
def updateServices(request, sid):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated, SellerPermission]
        service = ServiceModel.objects.get(id=sid)
        serializer = ServicesSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Service Details Updated", "data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["DELETE"])
def deleteServices(request, sid):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated, SellerPermission]
        user = SellerModel.objects.get(email=request.user.email)
        obj = ServiceModel.objects.get(id=sid)
        if obj.saloon.owner != user:
            return Response({"message":"You cannot delete this service"}, status=status.HTTP_401_UNAUTHORIZED)
        obj.delete()
        return Response({"message":"Service Deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def getServices(request, sal_id):
    try:
        objs = ServiceModel.objects.filter(saloon = SaloonModel.objects.get(id=sal_id))
        serializer = ServicesSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SeatLC(ListCreateAPIView):
    queryset = SeatModel.objects.all()
    serializer_class = SeatSerializer
    def list(self, request, sal_id):
        try:
            shop = SaloonModel.objects.get(id=sal_id)
            serializer = SeatSerializer(shop.saloon_seats.all(), many=True)
            return Response({"data":serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def create(self, request, sal_id):
        try:
            data = request.data
            authentication_classes = [JWTAuthentication]
            permission_classes = [IsAuthenticated, SellerPermission]
            serializer = SeatSerializer(data=data)
            if serializer.is_valid():
                serializer.save(saloon=SaloonModel.objects.get(id=sal_id))
                return Response({"message":"Seat added", "data":serializer.data}, status=status.HTTP_200_OK)
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SeatRUD(RetrieveAPIView):
    queryset = SeatModel.objects.all()
    serializer_class = SeatSerializer
    lookup_field = "id"


@api_view(["PATCH"])
def updateSeat(request, sid):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated, SellerPermission]
        user = SellerModel.objects.get(email=request.user.email)
        obj = SeatModel.objects.get(id=sid)
        if obj.saloon.owner != user:
            return Response({"message":"You cannot delete this service"}, status=status.HTTP_401_UNAUTHORIZED)
        seat = SeatModel.objects.get(id=sid)
        serializer = SeatSerializer(seat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Seat Details Updated", "data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["DELETE"])
def deleteSeat(request, sid):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated, SellerPermission]
        user = SellerModel.objects.get(email=request.user.email)
        obj = SeatModel.objects.get(id=sid)
        if obj.saloon.owner != user:
            return Response({"message":"You cannot delete this service"}, status=status.HTTP_401_UNAUTHORIZED)
        obj.delete()
        return Response({"message":"Seat Deleted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message":"Something went wrong", "error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
