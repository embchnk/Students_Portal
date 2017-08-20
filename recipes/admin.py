from django.contrib import admin
from .models import Recipe, Ingredient, Unit, Quantity
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Unit)
admin.site.register(Quantity)
