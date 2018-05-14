from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Parking(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.TextField()

class ParkingSpot(models.Model):
	id = models.AutoField(primary_key=True)
	parking_id = models.ForeignKey(to=Parking, on_delete=models.CASCADE)
	number = models.IntegerField()

class ParkingSpotState(models.Model):
	id = models.AutoField(primary_key=True)
	parking_spot_id = models.ForeignKey(to=ParkingSpot, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	state = models.IntegerField(choices=((0, 'Unknown'), (1, 'Freeing'), (2, 'Free'), (3, 'Taking'), (4, 'Taken')))

class Reservation(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	parking_spot_id = models.ForeignKey(to=ParkingSpot, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	begin = models.DateTimeField()
	end = models.DateTimeField()
	status = models.IntegerField(choices=((0, 'Active'), (1, 'UserCancelled'), (2, 'StaffCancelled')))
