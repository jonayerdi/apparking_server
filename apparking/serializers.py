from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation
from django.db import models
from django.utils import timezone

def object_list_as_dict(object_list):
    objects = []
    for obj in object_list:
        objects.append(obj.pk)
    return {"keys": objects}

def parking_list_as_dict(parking_list):
    parkings = []
    for parking in parking_list:
        parkings.append({"key": parking.pk, "name": parking.name})
    return {"parkings": parkings}

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
    for parking_spot in ParkingSpot.objects.filter(parking=parking.pk):
        parking_spots.append(parking_spot.pk)
    return {
            "pk": parking.pk,
            "name": parking.name,
            "parking_spots": parking_spots
            }

def parking_spot_as_dict(parking_spot):
    parking_spot_state = ParkingSpotState.objects.filter(parking_spot=parking_spot.pk).order_by('timestamp').last()
    reservation = Reservation.objects.filter(parking_spot=parking_spot.pk,begin__lte=timezone.now(), end__gt=timezone.now(), status=0).first()
    reservation_id = None
    if reservation:
        reservation_id = reservation.pk
    return {
            "pk": parking_spot.pk,
            "number": parking_spot.number,
            "reservation": reservation_id,
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
        return {}

def camera_list_as_dict(camera_list):
    cameras = []
    for camera in camera_list:
        cameras.append({"key": camera.pk, "number": camera.number})
    return {"cameras": cameras}

def reservation_as_dict(reservation):
    return {
        "pk": reservation.pk,
        "user": reservation.user.pk,
        "spot": reservation.parking_spot.pk,
        "timestamp": str(reservation.timestamp),
        "begin": str(reservation.begin),
        "end": str(reservation.end),
        "status": Reservation.STATUS_NAMES[reservation.status],
        }
