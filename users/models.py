from django.db import models

# Create your models here.
#first model for users

class User(models.Model):
    login = models.CharField(max_length=50)
    password= models.CharField(max_length=50)
    scores= models.IntegerField()

    def __str__(self):
        return self.login+'-'+self.password+'-'+str(self.scores)

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=250)
    likes= models.IntegerField()
    level= models.CharField(max_length=50)
    instructions = models.CharField(max_length=100000)
    dish_photo = models.CharField(max_length=10000)

    def __str__(self):
        return self.title+'-'+self.author.login + '-'+ str(self.likes)+ '-'+ str(self.level)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.ManyToManyField(Recipe)
    how_many = models.CharField(max_length=100)

    def __str__(self):
        return self.name+' - '+self.how_many