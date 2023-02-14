import threading
from django.conf import settings
from django.core.mail import send_mail
from .models import *

class send_booking_mail(threading.Thread):
    def __init__(self, email, timimg, service):
        self.email = email
        self.timimg = timimg
        self.service = service
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "Booking Successfull"
            message = f"Your booking for {self.service.service_name} at {self.service.saloon.name} was successfully booked for {self.timimg}."
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
            print(e)


class send_booking_mail_seller(threading.Thread):
    def __init__(self, email, seats, timimg):
        self.email = email
        self.seats = seats
        self.timimg = timimg
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "New Booking"
            message = f"New booking for {self.seats} at {self.timimg}."
            email_from = settings.EMAIL_HOST_USER
            print("Email send started")
            send_mail(subject , message ,email_from ,[self.email])
            print("Email send finished")
        except Exception as e:
            print(e)