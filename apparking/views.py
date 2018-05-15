from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation

def index(request):
    return render(request, 'index.html')

def api_users(request):
    users = User.objects.all()
    content = '{"Users": []}'
    return HttpResponse(content)

def api_user(request, pk):
    user = User.objects.filter(pk=pk)
    content = '{"User": "Data"}'
    return HttpResponse(content)
