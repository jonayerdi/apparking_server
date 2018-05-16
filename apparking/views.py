from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation
from .serializers import *
import json

def not_found(request, exception=None):
    return render(request, '404.html', status=404)

def index(request):
    if request.method == "GET":
        return render(request, 'index.html')
    return not_found(request)

def api_users(request):
    if request.method == "GET":
        profiles = Profile.objects.all()
        content = json.dumps(object_list_as_dict(profiles), indent=4)
        return HttpResponse(content, content_type='application/json')
    return not_found(request)

def api_user(request, pk):
    if request.method == "GET":
        profile = Profile.objects.filter(pk=pk).first()
        if profile:
            content = json.dumps(profile_as_dict(profile), indent=4)
            return HttpResponse(content=content, content_type='application/json')
    return not_found(request)

def api_parkings(request):
    if request.method == "GET":
        parkings = Parking.objects.all()
        content = json.dumps(object_list_as_dict(parkings), indent=4)
        return HttpResponse(content, content_type='application/json')
    return not_found(request)

def api_parking(request, pk):
    if request.method == "GET":
        parking = Parking.objects.filter(pk=pk).first()
        if parking:
            content = json.dumps(parking_as_dict(parking), indent=4)
            return HttpResponse(content=content, content_type='application/json')
    return not_found(request)

def api_reservations(request):
    if request.method == "GET":
        reservations = Reservation.objects.all()
        content = json.dumps(object_list_as_dict(reservations), indent=4)
        return HttpResponse(content, content_type='application/json')
    return not_found(request)
