from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Parking, ParkingSpot, ParkingSpotState, Reservation
from .serializers import UserSerializer
from rest_framework.renderers import JSONRenderer

def index(request):
    return render(request, 'index.html')

def api_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content)

def api_user(request, pk):
    user = User.objects.filter(pk=pk)
    serializer = UserSerializer(user)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content)
