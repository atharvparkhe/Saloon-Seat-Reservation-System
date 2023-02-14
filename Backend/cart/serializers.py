from rest_framework import serializers
from .models import *


class OrderUpdateSerializer(serializers.Serializer):
    order_id = serializers.CharField(required = True)
    is_completed = serializers.BooleanField(required = True)


class UserOrderSerializer(serializers.ModelSerializer):
    # cart_items = serializers.SerializerMethodField()
    class Meta:
        model = OrderModel
        exclude = ["owner", "updated_at"]
    # def get_cart_items(self, obj):
    #     items = []
    #     try:
    #         cart_items = obj.order_items.all()
    #         ser = OrderItemsSerializer(cart_items, many=True)
    #         items = ser.data
    #         return items
    #     except Exception as e:
    #         print(e)



class BookingSerializer(serializers.Serializer):
    service_id = serializers.CharField(required=True)
    # seats = serializers.CharField(required=True)
    date = serializers.DateField(required = True)


# class OrderItemsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItemModel
#         exclude = ["owner"]


class OrderSerializer(serializers.ModelSerializer):
    # cart_items = serializers.SerializerMethodField()
    class Meta:
        model = OrderModel
        exclude = ["owner", "updated_at"]
    # def get_cart_items(self, obj):
    #     cart_items = []
    #     try:
    #         cart_obj = OrderModel.objects.get(id = obj.id)
    #         serializer = OrderItemsSerializer(cart_obj.order_items.all(), many=True)
    #         cart_items = serializer.data
    #         return cart_items
    #     except Exception as e:
    #         print(e)
