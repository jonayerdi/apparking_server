from django.contrib import admin
from .models import Parking, ParkingSpot, ParkingSpotState, Reservation

admin.site.register(Parking)
admin.site.register(ParkingSpot)
admin.site.register(ParkingSpotState)
admin.site.register(Reservation)
