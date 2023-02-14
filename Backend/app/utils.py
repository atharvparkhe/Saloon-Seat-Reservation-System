from .models import *
import random, uuid

def addSeats(saloon_id):
    try:
        saloon = SaloonModel.objects.get(id=saloon_id)
        for i in range(5):
            SeatModel.objects.create(
                saloon = saloon,
                seat_name = str(saloon.name) + "_" + str(i),
                is_available = True
            )
    except Exception as e:
        print(e)


def generateServices(saloon_id):
    try:
        saloon = SaloonModel.objects.get(id=saloon_id)
        for i in range(5):
            ServiceModel.objects.create(
                saloon = saloon,
                service_name = " Service  " + str(i) + str(uuid.uuid4()).split("-")[0],
                service_cost = random.randint(40, 250),
                service_duration = "0:30:0"
            )
    except Exception as e:
        print(e)