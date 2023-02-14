from rest_framework import serializers
from .models import *


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatModel
        exclude = ["created_at", "updated_at", "saloon"]

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceModel
        exclude = ["created_at", "updated_at", "saloon"]

class MultiSaloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaloonModel
        fields = ["id", "name", "description", "logo"]

class SaloonGetSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = SaloonModel
        exclude = ["owner"]

class SaloonNameSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = SaloonModel
        fields = ["name"]

class SaloonSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField()
    class Meta:
        model = SaloonModel
        exclude = ["created_at", "updated_at", "owner", "address", "town", "state", "pincode"]
    def get_seats(self, obj):
        seats = 0
        try:
            saloon = SaloonModel.objects.get(id = obj.id)
            seats = saloon.saloon_seats.filter(is_available=True).count()
            return seats
        except Exception as e:
            print(e)

class SaloonSerializer1(serializers.ModelSerializer):
    class Meta:
        model = SaloonModel
        exclude = ["created_at", "updated_at", "owner"]


class SeatingSerializer(serializers.Serializer):
    saloon_id = serializers.CharField(required=True)


class AddSeatSerializer(serializers.Serializer):
    restaurant_id = serializers.CharField(required=True)
    seat_name = serializers.CharField(required = True)
