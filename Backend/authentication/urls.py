from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('signup/', views.signUp, name="signup"),
	path('login/', views.logIn, name="login"),
	path('forgot/', views.forgot, name="forgot"),
	path('reset/<uid>/', views.reset, name="reset"),

	path('seller-signup/', views.sellerSignUp, name="seller-signup"),
	path('seller-verify/<uid>/', views.sellerVerify, name="seller-verify"),
	path('seller-login/', views.sellerLogIn, name="seller-login"),
	path('seller-forgot/', views.sellerForgot, name="seller-forgot"),
	path('seller-reset/<uid>/', views.sellerReset, name="seller-reset"),

	# path('address/', views.AddressAPI.as_view(), name="address"),
	
	# path('seller-login/otp/', views.sellerLogInOTP, name="seller-login-otp"),
	# path('worker-signup/', views.workerSignUp, name="worker-signup"),
	# path('worker-verify/<uid>/', views.workerVerify, name="worker-verify"),
	# path('worker-login/', views.workerLogIn, name="worker-login"),
	# path('worker-login/otp/', views.workerLogInOTP, name="worker-login-otp"),
	# path('worker-forgot/', views.workerForgot, name="worker-forgot"),
	# path('worker-reset/<uid>/', views.workerReset, name="worker-reset"),
]