from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render
from .models import *
from .threads import *
from .serializers import *


@api_view(["POST"])
def signUp(request):
    try:
        data = request.data
        serializer = signupSerializer(data=data)
        if serializer.is_valid():
            name = serializer.data["name"]
            email = serializer.data["email"]
            password = serializer.data["password"]
            if CustomerModel.objects.filter(email=email).first():
                return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            new_customer = CustomerModel.objects.create(email=email, name=name)
            new_customer.set_password(password)
            new_customer.save()
            return Response({"message":"Account created"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def logIn(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = str(serializer.data["email"]).lower()
            password = serializer.data["password"]
            customer_obj = CustomerModel.objects.filter(email=email).first()
            if customer_obj is None:
                print("Account does not exist")
                return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if not user:
                print("Incorrect password")
                return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            print(jwt_token.access_token)
            return Response({"message":"Login successfull", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def forgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user = CustomerModel.objects.get(email=email)
            if not user:
                return Response({"message":"Account does not exists"}, status=status.HTTP_404_NOT_FOUND)
            otp = uuid.uuid4()
            user.token = otp
            user.save()
            thread_obj = send_forgot_email_customer(email, otp)
            thread_obj.start()
            return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(["POST"])
def reset(request, uid):
    try:
        context = {}
        user_obj = CustomerModel.objects.get(token=uid)
        if not user_obj:
            context["data"] = "Account does not exist"
            return render(request, "failed.html", context)
        if request.method == 'POST':
            npw = request.POST.get("npw")
            cpw = request.POST.get("cpw")
            if npw == cpw:
                user_obj.set_password(cpw)
                user_obj.save()
                context["data"] = "Password Change"
                return render(request, "success.html", context)
            return render(request, "failed.html", {"data":"Passwords don't Not Match"})
    except Exception as e:
        context["data"] = "Something Went Wrong. Error : " + str(e)
        return render(request, "failed.html", context)
    return render(request, "reset.html")

#################################################################################################################################################
#################################################################################################################################################

@api_view(["POST"])
def sellerSignUp(request):
    try:
        data = request.data
        serializer = signupSerializer(data=data)
        if serializer.is_valid():
            name = serializer.data["name"]
            email = serializer.data["email"]
            phone = serializer.data["phone"]
            gst = serializer.data["gst"]
            if SellerModel.objects.filter(email=email).first():
                return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            otp = uuid.uuid4()
            obj = SellerModel.objects.create(email=email, name=name, phone=phone, gst_number=gst, token=otp)
            thread_obj = send_verification_email_seller(email, otp)
            thread_obj.start()
            obj.set_password(serializer.data["password"])
            obj.save()
            return Response({"message":"Account created. Verification link sent on your mail"}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def sellerVerify(request, uid):
    try:
        context = {}
        obj = SellerModel.objects.get(token=uid)
        if not obj:
            context["data"] = "Account does not exist"
            return render(request, "failed.html", context)
        if obj.is_verified == True:
            context["data"] = "Account already verified"
            return render(request, "failed.html", context)
        obj.is_verified = True
        obj.save()
        context["data"] = "Verification Successfull"
        return render(request, "success.html", context)
    except Exception as e:
        context["data"] = "Something Went Wrong. Error : " + str(e)
        return render(request, "failed.html", context)


@api_view(["POST"])
def sellerLogIn(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            password = serializer.data["password"]
            obj = SellerModel.objects.filter(email=email).first()
            if obj is None:
                return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            if not obj.is_verified:
                return Response({"message":"Email not verified. Check your mail"}, status=status.HTTP_401_UNAUTHORIZED)
            user = authenticate(email=email, password=password)
            if not user:
                return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            return Response({"message":"Login successfull", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def sellerForgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user = SellerModel.objects.get(email=email)
            if not user:
                return Response({"message":"Account does not exists"}, status=status.HTTP_404_NOT_FOUND)
            otp = uuid.uuid4()
            user.token = otp
            user.save()
            thread_obj = send_forgot_email(email, otp)
            thread_obj.start()
            return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def sellerReset(request, uid):
    try:
        context = {}
        if not SellerModel.objects.filter(token=uid).first():
            context["data"] = "Account does not exist"
            return render(request, "failed.html", context)
        user_obj = SellerModel.objects.get(token=uid)
        if request.method == 'POST':
            npw = request.POST.get("npw")
            cpw = request.POST.get("cpw")
            if npw == cpw:
                user_obj.set_password(cpw)
                user_obj.save()
                context["data"] = "Password Change"
                return render(request, "success.html", context)
            return render(request, "failed.html", {"data":"Passwords don't Not Match"})
    except Exception as e:
        context["data"] = "Something Went Wrong. Error : " + str(e)
        return render(request, "failed.html", context)
    return render(request, "reset.html")

# @api_view(["POST"])
# def sellerLogInOTP(request):
#     try:
#         data = request.data
#         serializer = otpSerializer(data=data)
#         if serializer.is_valid():
#             password = serializer.data["pw"]
#             otp = serializer.data["otp"]
#             user_email = cache.get(otp)
#             if not cache.get(otp):
#                 return Response({"message":"OTP invalid or expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
#             obj = SellerModel.objects.filter(email=user_email).first()
#             if obj is None:
#                 return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
#             if not obj.is_verified:
#                 return Response({"message":"Email not verified"}, status=status.HTTP_401_UNAUTHORIZED)
#             user = authenticate(email=user_email, password=password)
#             if not user:
#                 return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#             jwt_token = RefreshToken.for_user(user)
#             return Response({"message":"Login successfull", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
#         return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#################################################################################################################################################

# class AddressAPI(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         try:
#             user_obj = CustomerModel.objects.get(email=request.user.email)
#             obj = user_obj.customer_address.all()
#             serializer = AddressSerializer(obj, many=True)
#             return Response({"data":serializer.data, "message":"customer address"}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error":str(e), "message":"something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     def post(self, request):
#         try:
#             data = request.data
#             user_obj = CustomerModel.objects.get(email=request.user.email)
#             serializer = AddressSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save(customer=user_obj)
#                 return Response({"data":serializer.data, "message":"address added"}, status=status.HTTP_201_CREATED)
#             return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error":str(e), "message":"something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     def patch(self, request):
#         try:
#             data = request.data
#             user_obj = CustomerModel.objects.get(email=request.user.email)
#             obj = CustomerAddress.objects.get(id = data["id"])
#             serializer = AddressSerializer(obj, data=data, partial=True)
#             if serializer.is_valid():
#                 serializer.save(customer=user_obj)
#                 return Response({"data":serializer.data, "message":"address updated"}, status=status.HTTP_202_ACCEPTED)
#             return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error":str(e), "message":"something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#################################################################################################################################################

#################################################################################################################################################

# @api_view(["POST"])
# def workerSignUp(request):
#     try:
#         data = request.data
#         serializer = signupSerializer(data=data)
#         if serializer.is_valid():
#             name = serializer.data["name"]
#             email = serializer.data["email"]
#             phone = serializer.data["phone"]
#             start_timings = serializer.data["start_timings"]
#             end_timings = serializer.data["end_timings"]
#             img = serializer.data["profile_img"]
#             password = serializer.data["password"]
#             if WorkerModel.objects.filter(email=email).first():
#                 return Response({"message":"Acount already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
#             obj = WorkerModel.objects.create(email=email, name=name, phone=phone, profile_img=img, start_timings=start_timings, end_timings=end_timings)
#             obj.set_password(password)
#             thread_obj = send_worker_verification_email(email)
#             thread_obj.start()
#             obj.save()
#             return Response({"message":"Account created. Verification link sent on your mail"}, status=status.HTTP_201_CREATED)
#         return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def workerVerify(request, uid):
#     try:
#         context = {}
#         if not cache.get(uid):
#             context["data"] = "Link invalid or expired"
#             return render(request, "failed.html", context)
#         obj = WorkerModel.objects.filter(email=cache.get(uid)).first()
#         if obj is None:
#             context["data"] = "Account does not exist"
#             return render(request, "failed.html", context)
#         obj.is_verified = True
#         obj.save()
#         context["data"] = "Verification"
#         return render(request, "success.html", context)
#     except Exception as e:
#         context["data"] = "Something Went Wrong. Error : " + str(e)
#         return render(request, "failed.html", context)


# @api_view(["POST"])
# def workerLogIn(request):
#     try:
#         data = request.data
#         serializer = emailSerializer(data=data)
#         if serializer.is_valid():
#             email = serializer.data["email"]
#             obj = WorkerModel.objects.filter(email=email).first()
#             if obj is None:
#                 return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
#             if not obj.is_verified:
#                 return Response({"message":"Email not verified. Check your mail"}, status=status.HTTP_401_UNAUTHORIZED)
#             thread_obj = send_login_otp(email)
#             thread_obj.start()
#             return Response({"message":"Login OTP sent"}, status=status.HTTP_202_ACCEPTED)
#         return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def workerLogInOTP(request):
#     try:
#         data = request.data
#         serializer = otpSerializer(data=data)
#         if serializer.is_valid():
#             password = serializer.data["pw"]
#             otp = serializer.data["otp"]
#             user_email = cache.get(otp)
#             if not cache.get(otp):
#                 return Response({"message":"OTP invalid or expired"}, status=status.HTTP_408_REQUEST_TIMEOUT)
#             obj = WorkerModel.objects.filter(email=user_email).first()
#             if obj is None:
#                 return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
#             if not obj.is_verified:
#                 return Response({"message":"Email not verified"}, status=status.HTTP_401_UNAUTHORIZED)
#             user = authenticate(email=user_email, password=password)
#             if not user:
#                 return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#             jwt_token = RefreshToken.for_user(user)
#             return Response({"message":"Login successfull", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
#         return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def workerForgot(request):
#     try:
#         data = request.data
#         serializer = emailSerializer(data=data)
#         if serializer.is_valid():
#             email = serializer.data["email"]
#             if not WorkerModel.objects.get(email=email):
#                 return Response({"message":"Account does not exists"}, status=status.HTTP_404_NOT_FOUND)
#             thread_obj = send_worker_forgot_email(email)
#             thread_obj.start()
#             return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
#         return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def workerReset(request, uid):
#     try:
#         context = {}
#         if not cache.get(uid):
#             context["data"] = "Link invalid or expired"
#             return render(request, "failed.html", context)
#         if not WorkerModel.objects.filter(email=cache.get(uid)).first():
#             context["data"] = "Account does not exist"
#             return render(request, "failed.html", context)
#         user_obj = WorkerModel.objects.get(email=cache.get(uid))
#         if request.method == 'POST':
#             pw = request.POST.get("npw")
#             cpw = request.POST.get("cpw")
#             if pw == cpw:
#                 user_obj.set_password(cpw)
#                 user_obj.save()
#                 context["data"] = "Password Change"
#                 return render(request, "success.html", context)
#             return render(request, "failed.html", {"data":"Passwords don't Not Match"})
#     except Exception as e:
#         context["data"] = "Something Went Wrong. Error : " + str(e)
#         return render(request, "failed.html", context)
#     return render(request, "reset.html")

