from django.db import models
from django.contrib.auth.models import User

# every user can set his default city
class Location(models.Model):
    city_name = models.CharField(max_length=200)
    longiture = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)

# class extending class User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    points = models.IntegerField()


