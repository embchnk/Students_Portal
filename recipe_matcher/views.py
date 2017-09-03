from django.shortcuts import render
from recipes.models import *


def match_recipes(request):
    result = request.GET.getlist('ingredients')
    matched_recipes = {}
    for ingredient in result:
        for recipe in Ingredient.objects.get(id=ingredient).recipe.all():
            try:
                matched_recipes[recipe] += 1
            except KeyError:
                matched_recipes[recipe] = 1
    return render(request, 'recipes/bookRecipes.html', {'all_recipes': reversed(sorted(matched_recipes, key=matched_recipes.__getitem__))})
