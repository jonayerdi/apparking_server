from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import IsPhoneValidator

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=9,  validators=[IsPhoneValidator])
	email = models.EmailField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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
