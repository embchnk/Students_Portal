from django.shortcuts import render, get_object_or_404
from recipes.models import *
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user


def match_recipes(request):
    result = request.GET.getlist('selectedingredient')
    matched_recipes = {}
    for ingredient in result:
        for recipe in Ingredient.objects.get(id=ingredient).recipe.all():
            try:
                matched_recipes[recipe] += 1
            except KeyError:
                matched_recipes[recipe] = 1
    request.session['ingredients'] = result
    return render(request, 'recipes/bookRecipes.html', {'all_recipes': reversed(sorted(matched_recipes, key=matched_recipes.__getitem__))})
