from .models import Recipe, Ingredient, Unit, Quantity
from users.models import Profile, User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth import get_user
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from users.forms import LoginForm


# Create your views here.
def bookRecipes(request):
    all_recipes = Recipe.objects.all()
    context = {
        'all_recipes': all_recipes
    }
    return render(request, 'recipes/bookRecipes.html', context)


# my single recipe
def single_recipe(request, recipe_id):
    # try:
    #    single_recipe = Recipe.objects.get(pk=recipe_id)
    # except Recipe.DoesNotExist:
    #    raise Http404
    single_recipe = get_object_or_404(Recipe, pk=recipe_id)
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

    return render(request, 'recipes/single_recipe.html', {'single_recipe': single_recipe, 'dict': dict})


def new_recipe(request):
    if request.user is not None:
        if request.user.is_authenticated:
            return render(request, 'recipes/recipe_form.html', {'unit_class': Unit.objects.all()})
        return render(request, 'users/login_form.html', {'form': LoginForm, 'LogInMsg': 'You need to log in to add recipe'})


def favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    try:
        if recipe.likes == 1:
            recipe.likes = 0
        else:
            recipe.likes = 1
        recipe.save()
    except (KeyError, Recipe.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def result_of_addition_recipe(request):
    u = get_user(request)
    if u is not None:
        if u.is_authenticated and request.POST['name'] and request.POST['i0'] and request.POST['instruction']:
            profile = Profile.objects.get(user=u)
            new_recipe = Recipe(author=profile, title=request.POST['name'], likes=0,
                                instruction=request.POST['instruction'], level=request.POST['level'])
            new_recipe.save()
            for i in range(int(request.POST['number']) + 1):
                ingredient_index = "i" + str(i)
                unit_index = "unit" + str(i)
                quantity_index = "quantity" + str(i)
                try:
                    ingredient = Ingredient.objects.get(name=request.POST[ingredient_index])
                except Ingredient.DoesNotExist:
                    ingredient = Ingredient(name=request.POST[ingredient_index])
                    ingredient.save()
                try:
                    unit = Unit.objects.get(unit=request.POST[unit_index])
                except Unit.DoesNotExist:
                    unit = Unit(unit=request.POST[unit_index])
                    unit.save()
                try:
                    quantity = Quantity.objects.get(value=request.POST[quantity_index])
                except Quantity.DoesNotExist:
                    quantity = Quantity(value=request.POST[quantity_index])
                    quantity.save()
                ingredient.recipe.add(new_recipe)
                unit.recipe.add(new_recipe)
                unit.ingredient.add(ingredient)
                quantity.recipe.add(new_recipe)
                quantity.ingredient.add(ingredient)
            return render(request, 'recipes/recipe_form.html', {'result': 'True', 'unit_class': Unit.objects.all()})
        else:
            return render(request, 'recipes/recipe_form.html', {'result': 'False', 'unit_class': Unit.objects.all()})
    else:
        return redirect('users:index')
