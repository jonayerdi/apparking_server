from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation
from .serializers import *
import json

#Errors
def not_found(request, exception=None):
    return render(request, '404.html', status=404)

#Web Pages
def index(request):
    if request.method == "GET":
        return render(request, 'index.html')
    return not_found(request)

def parkings(request, pk):
    if request.method == "GET":
        parking = Parking.objects.filter(pk=pk).first()
        if parking:
            return render(request, 'parkings.html', {'parkingId': parking.pk})
    return not_found(request)

#REST API
def api_users(request):
    content = None
    if request.method == "GET":
        user_id = request.GET.get("id", "")
        name = request.GET.get("name", "")
        if user_id != "":
            profile = Profile.objects.filter(pk=user_id).first()
            if profile:
                content = json.dumps(profile_as_dict(profile), indent=4)
        elif name != "":
            user = User.objects.filter(username=name).first()
            if user:
                profile = Profile.objects.filter(user=user).first()
                if profile:
                    content = json.dumps(profile_as_dict(profile), indent=4)
        else:
            profiles = Profile.objects.all()
            content = json.dumps(object_list_as_dict(profiles), indent=4)
    if content:
        return HttpResponse(content=content, content_type='application/json')
    else:
        return not_found(request)

def api_parkings(request):
    content = None
    if request.method == "GET":
        parking_id = request.GET.get("id", "")
        spot_id = request.GET.get("spot", "")
        names = request.GET.get("names", "")
        if parking_id != "":
            parking = Parking.objects.filter(pk=parking_id).first()
            if parking:
                content = json.dumps(parking_as_dict(parking), indent=4)
        elif spot_id != "":
            spot = ParkingSpot.objects.filter(pk=spot_id).first()
            if spot:
                content = json.dumps(parking_spot_as_dict(spot), indent=4)
        else:
            parkings = Parking.objects.all()
            if names == "1":
                content = json.dumps(parking_list_as_dict(parkings), indent=4)
            else:
                content = json.dumps(object_list_as_dict(parkings), indent=4)
    if content:
        return HttpResponse(content=content, content_type='application/json')
    else:
        return not_found(request)

def api_reservations(request):
    content = None
    if request.method == "GET":
        reservation_id = request.GET.get("id", "")
        if reservation_id != "":
            reservation = Reservation.objects.filter(pk=reservation_id).first()
            if reservation:
                content = json.dumps(reservation_as_dict(reservation), indent=4)
        else:
            reservations = Reservation.objects.all()
            content = json.dumps(object_list_as_dict(reservations), indent=4)
    if content:
        return HttpResponse(content=content, content_type='application/json')
    else:
        return not_found(request)
