from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    city_name = models.CharField(max_length=200)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)

# class extending class User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    points = models.IntegerField(default=0)
    location = models.ForeignKey(Location, models.DO_NOTHING, null=True)