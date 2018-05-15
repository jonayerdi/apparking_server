from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation
from .serializers import *
import json

def index(request):
    return render(request, 'index.html')

def api_users(request):
    profiles = Profile.objects.all()
    content = json.dumps(object_list_as_dict(profiles), indent=4)
    return HttpResponse(content, content_type='application/json')

def api_user(request, pk):
    profile = Profile.objects.filter(pk=pk).first()
    if profile:
        content = json.dumps(profile_as_dict(profile), indent=4)
        return HttpResponse(content=content, content_type='application/json')
    else:
        return HttpResponse(status=404)

def api_parkings(request):
    parkings = Parking.objects.all()
    content = json.dumps(object_list_as_dict(parkings), indent=4)
    return HttpResponse(content, content_type='application/json')

def api_parking(request, pk):
    parking = Parking.objects.filter(pk=pk).first()
    if parking:
        content = json.dumps(parking_as_dict(parking), indent=4)
        return HttpResponse(content=content, content_type='application/json')
    else:
        return HttpResponse(status=404)

def api_reservations(request):
    reservations = Reservation.objects.all()
    content = json.dumps(object_list_as_dict(reservations), indent=4)
    return HttpResponse(content, content_type='application/json')

