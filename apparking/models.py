from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import IsPhoneValidator

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=9,  validators=[IsPhoneValidator])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Parking(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.TextField(unique=True)
	dataFolder = models.TextField(unique=True)

class ParkingSpot(models.Model):
	id = models.AutoField(primary_key=True)
	parking = models.ForeignKey(to=Parking, on_delete=models.CASCADE)
	number = models.IntegerField(default=0)
	class Meta:
		unique_together = (('parking', 'number'))

@receiver(post_save, sender=ParkingSpot)
def create_parking_spot_state(sender, instance, created, **kwargs):
    if created:
        ParkingSpotState.objects.create(parking_spot=instance)

class ParkingSpotState(models.Model):
	STATES = ((0, 'Unknown'), (1, 'Freeing'), (2, 'Free'), (3, 'Taking'), (4, 'Taken'))
	STATE_NAMES = {e[0]: e[1] for e in STATES}
	STATE_CODES = {e[1]: e[0] for e in STATES}
	id = models.AutoField(primary_key=True)
	parking_spot = models.ForeignKey(to=ParkingSpot, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	state = models.IntegerField(choices=STATES, default=0)
	forced = models.BooleanField(default=False)

class ParkingCamera(models.Model):
	id = models.AutoField(primary_key=True)
	parking = models.ForeignKey(to=Parking, on_delete=models.CASCADE)
	number = models.IntegerField(default=0)
	dataFolder = models.TextField(unique=True)
	class Meta:
		unique_together = (('parking', 'number'))

class ParkingCameraSpot(models.Model):
	id = models.AutoField(primary_key=True)
	camera = models.ForeignKey(to=ParkingCamera, on_delete=models.CASCADE)
	parking_spot = models.ForeignKey(to=ParkingSpot, on_delete=models.CASCADE)
	code = models.IntegerField(default=0)
	class Meta:
		unique_together = (('camera', 'parking_spot'))

class Reservation(models.Model):
	STATUS = ((0, 'Active'), (1, 'UserCancelled'), (2, 'StaffCancelled'))
	STATUS_NAMES = {e[0]: e[1] for e in STATUS}
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	parking_spot = models.ForeignKey(to=ParkingSpot, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	begin = models.DateTimeField()
	end = models.DateTimeField()
	status = models.IntegerField(choices=STATUS, default=0)
