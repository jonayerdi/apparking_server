from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation

def profile_list_as_dict(profile_list):
    profiles = []
    for profile in profile_list:
        profiles.append(profile.pk)
    return {"users": profiles}

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

def parking_list_as_dict(parking_list):
    parkings = []
    for parking in parking_list:
        parkings.append(parking.pk)
    return {"parkings": parkings}

def parking_as_dict(parking):
    return {
        "pk": parking.pk,
        "name": parking.name
    }
