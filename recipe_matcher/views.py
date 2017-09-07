from django.shortcuts import render, get_object_or_404
from recipes.models import *
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user


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
    missing = {}
    for ingredient in Ingredient.objects.get(recipe=single_recipe):
        if ingredient not in ingredients:
            missing[ingredient] = 1

    # code copied from single_recipe view
    thumb_is_up = False

    try:
        u = get_user(request)
        if single_recipe.likes.filter(user=u).count():
            thumb_is_up = True
    except:
        # this line of code is unnecessary but I must write except
        thumb_is_up = False

    dict = {}
    for i in range(single_recipe.ingredient_set.count()):
        ingredient = single_recipe.ingredient_set.all()[i]
        try:
            temp_quantity = Quantity.objects.filter(recipe=single_recipe, ingredient=ingredient).values_list('value',
                                                                                                             flat=True).get()
        except MultipleObjectsReturned:
            temp_quantity = \
                Quantity.objects.filter(recipe=single_recipe, ingredient=ingredient).values_list('value', flat=True)[0]
        try:
            temp_unit = Unit.objects.filter(recipe=single_recipe, ingredient=ingredient).values_list('unit',
                                                                                                     flat=True).get()
        except MultipleObjectsReturned:
            temp_unit = Unit.objects.filter(recipe=single_recipe, ingredient=ingredient).values_list('unit', flat=True)[
                0]
        dict[ingredient] = str(temp_quantity) + " " + str(temp_unit)

        return render(request, 'recipes/single_recipe.html',
                      {'single_recipe': single_recipe, 'dict': dict, 'missing': missing, 'thumb_is_up': thumb_is_up})
