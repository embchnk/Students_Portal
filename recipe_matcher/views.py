from django.shortcuts import render, get_object_or_404
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
    request.session['ingredients'] = result
    return render(request, 'recipes/bookRecipes.html', {'all_recipes': reversed(sorted(matched_recipes, key=matched_recipes.__getitem__))})


# view similar to single_recipe but also storing information about missing_ingredients (hope it works)
# need to change template to one showing missing_ingredients list
def matched_recipe(request, recipe_id):
    single_recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = request.session.pop('ingredient', None)
    request.session.modified = True
    missing_ingredients = []
    for ingredient in Ingredient.objects.get(recipe=single_recipe):
        if ingredient not in ingredients:
            missing_ingredients.append(ingredient)
    return render(request, 'recipes/single_recipe.html', {'missing_ingredients': missing_ingredients})
