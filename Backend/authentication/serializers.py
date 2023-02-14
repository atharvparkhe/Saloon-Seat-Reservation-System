from rest_framework import serializers
from .models import *
from .validators import validate_pw, validate_name


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)


class signupSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    phone = serializers.IntegerField(required = False)
    gst = serializers.IntegerField(required = False)
    password = serializers.CharField(required = True)
    def validate(self, data):
        validate_pw(data["password"])
        validate_name(data["name"])
        return data


class otpSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required = True)
    pw = serializers.CharField(required = False)
    cpw = serializers.CharField(required = False)
    # def validate(self, data):
        # validate_pw(data["pw"])
        # validate_pw(data["cpw"])
        # return data

class PWserializer(serializers.Serializer):
    npw = serializers.CharField(required = False)
    cpw = serializers.CharField(required = False)


class emailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomerAddress
#         exclude = ["customer", "created_at", "updated_at"]


class CustomerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ["name"]


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ["name", "email", "phone"]
