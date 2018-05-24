from django.contrib import admin
from .models import Profile, Parking, ParkingSpot, ParkingSpotState, ParkingCamera, Reservation

admin.site.register(Profile)
admin.site.register(Parking)
admin.site.register(ParkingSpot)
admin.site.register(ParkingSpotState)
admin.site.register(ParkingCamera)
admin.site.register(Reservation)
