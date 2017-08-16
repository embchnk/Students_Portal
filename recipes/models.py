from django.db import models
from users.models import Profile

# Create your models here.

class Recipe(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title= models.CharField(max_length=250)
    likes= models.IntegerField()
    level= models.CharField(max_length=50)
    instruction = models.CharField(max_length=100000)
    dish_photo = models.CharField(max_length=10000)

    def __str__(self):
        return self.title+'-'+self.author.user.first_name+ '-'+ str(self.likes)+ '-'+ str(self.level)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.ManyToManyField(Recipe)
    how_many = models.CharField(max_length=100)

    def __str__(self):
        return self.name+' - '+self.how_many