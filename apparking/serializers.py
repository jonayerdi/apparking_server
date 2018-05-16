from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation
from django.db import models

def object_list_as_dict(object_list):
    objects = []
    for obj in object_list:
        objects.append(obj.pk)
    return {"keys": objects}

def profile_as_dict(profile):
    return {
        "pk": profile.pk,
        "username": profile.user.username,
        "first_name": profile.user.first_name,
        "last_name": profile.user.last_name,
        "email": profile.user.email,
        "is_staff": profile.user.is_staff,
        "is_active": profile.user.is_active,
        "date_joined": str(profile.user.date_joined),
        "last_login": str(profile.user.last_login),
        "phone": profile.phone
        }

def parking_as_dict(parking):
    parking_spots = []
    for parking_spot in ParkingSpot.objects.filter(parking_id=parking.pk):
        parking_spots.append(parking_spot.pk)
    return {
            "pk": parking.pk,
            "name": parking.name,
            "parking_spots": parking_spots
            }

def parking_spot_as_dict(parking_spot):
    parking_spot_state = ParkingSpotState.objects.filter(parking_spot_id=parking_spot.pk).order_by('timestamp').last()
    return {
            "pk": parking_spot.pk,
            "name": parking_spot.name,
            "state": parking_spot_state_as_dict(parking_spot_state)
            }

def parking_spot_state_as_dict(parking_spot_state):
    if parking_spot_state:
        return {
                "state": ParkingSpotState.STATE_NAMES[parking_spot_state.state],
                "forced": parking_spot_state.forced,
                "timestamp": str(parking_spot_state.timestamp)
                }
    else:
        return {
                "state": None,
                "forced": None,
                "timestamp": None
                }

def reservation_as_dict(reservation):
    return {
        "pk": reservation.pk,
        "user": reservation.user,
        "spot": reservation.parking_spot_id,
        "timestamp": str(reservation.timestamp),
        "begin": str(reservation.begin),
        "end": str(reservation.end),
        "status": Reservation.STATUS_NAMES[reservation.status],
        }
