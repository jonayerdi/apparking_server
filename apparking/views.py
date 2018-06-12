from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Profile, Parking, ParkingSpot, ParkingSpotState, ParkingCamera, Reservation
from .serializers import *
import json
from datetime import datetime
import os

#Apparking camera images location
CAMERAS_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cameras')

#Errors
def not_found(request, exception=None):
    return render(request, '404.html', status=404)

#Authentication
def login_user(request):
    logout(request)
    username = password = None
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
    elif request.GET:
        username = request.GET['username']
        password = request.GET['password']

    if username and password:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
    return not_found(request)

def logout_user(request):
    logout(request)
    return redirect('/')

#Web Pages
def index(request):
    return redirect('/parkings')

def parkings_list(request):
    if request.method == "GET":
        return render(request, 'parkingsList.html')
    return not_found(request)

def parking(request, pk):
    if request.method == "GET":
        parking = Parking.objects.filter(pk=pk).first()
        if parking:
            if request.GET.get("text", "") != "":
                return render(request, 'parking.html', {'parkingId': parking.pk})
            else:
                return render(request, 'parkingLayout.html', {'parkingId': parking.pk})
    return not_found(request)

def camera_list(request):
    if request.method == "GET":
        return render(request, 'camerasList.html')
    return not_found(request)

def camera(request, pk):
    if request.method == "GET":
        camera = ParkingCamera.objects.filter(pk=pk).first()
        if camera:
            return render(request, 'camera.html', {'cameraId': camera.pk})
    return not_found(request)

#Camera images
@never_cache
def camera_image(request, pk):
    if request.method == "GET":
        try:
            camera = ParkingCamera.objects.filter(pk=pk).first()
            if camera:
                file_path = os.path.join(CAMERAS_ROOT, camera.dataFolder, 'image.png')
                with open(file_path, 'rb') as fsock:
                    response = HttpResponse(content=fsock.read(), content_type='image/png')
                response["Cache-Control"] = "no-cache, no-store, must-revalidate"
                response['Pragma'] = 'no-cache'
                return response
        except Exception:
            pass
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

def api_cameras(request):
    content = None
    if request.method == "GET":
        camera_id = request.GET.get("id", "")
        if camera_id != "":
            camera = ParkingCamera.objects.filter(pk=camera_id).first()
            if camera:
                content = json.dumps(camera_as_dict(camera), indent=4)
        else:
            parking_id = request.GET.get("parking", "")
            if parking_id != "":
                cameras = ParkingCamera.objects.filter(pk=parking_id)
            else:
                cameras = ParkingCamera.objects.all()
            content = json.dumps(camera_list_as_dict(cameras), indent=4)
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
    elif request.method == "POST":
        if request.user.is_authenticated():
            reservation = Reservation.objects.filter(user=request.user, begin__lte=timezone.now(), end__gt=timezone.now(), status=0).first()
            if reservation:
                return HttpResponse(content=json.dumps({"message": "user has a reservation already"}), content_type='application/json')
            else:
                begin = datetime.strptime(request.POST.get("begin", ""), '%Y-%m-%d %H:%M')
                end = datetime.strptime(request.POST.get("end", ""), '%Y-%m-%d %H:%M')
                spot_id = request.POST.get("spot", "")
                spot = ParkingSpot.objects.filter(pk=spot_id).first()
                if not spot:
                    return HttpResponse(content=json.dumps({"message": "parking spot not found"}), content_type='application/json')
                elif end-begin > datetime.timedelta.__new__(hours=4):
                    return HttpResponse(content=json.dumps({"message": "reservation timespan too long"}), content_type='application/json')
                else:
                    reservation = Reservation(user=request.user, parking_spot=spot, begin=begin, end=end)
                    reservation.save()
                    return HttpResponse(content=json.dumps({"message": "ok"}), content_type='application/json')
        else:
            return HttpResponse(content=json.dumps({"message": "user must be authenticated for this api"}), content_type='application/json')
    if content:
        return HttpResponse(content=content, content_type='application/json')
    else:
        return not_found(request)
