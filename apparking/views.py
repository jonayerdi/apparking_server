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
    content = json.dumps(profile_list_as_dict(profiles), indent=4)
    return HttpResponse(content, content_type='application/json')

def api_user(request, pk):
    profiles = Profile.objects.filter(pk=pk)
    if profiles:
        profile = profiles[0]
        content = json.dumps(profile_as_dict(profile), indent=4)
        return HttpResponse(content=content, content_type='application/json')
    else:
        return HttpResponse(status=404)
