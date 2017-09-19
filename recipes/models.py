from django.db import models
from users.models import Profile


class Recipe(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author', blank=True, null=True)
    title = models.CharField(max_length=250)
    likes = models.ManyToManyField(Profile, blank=True, related_name='likes')
    level = models.CharField(max_length=50)
    instruction = models.CharField(max_length=100000)
    dish_photo = models.FileField(null=True, default='recipe_default.png')

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    recipe = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    unit = models.CharField(max_length=100)
    recipe = models.ManyToManyField(Recipe, blank=True)
    ingredient = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        return self.unit


class Quantity(models.Model):
    value = models.IntegerField()
    recipe = models.ManyToManyField(Recipe, blank=True)
    ingredient = models.ManyToManyField(Ingredient, blank=True)

    def __str__(self):
        return str(self.value)


