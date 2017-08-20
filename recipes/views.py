from .models import Recipe, Ingredient, Unit, Quantity
from users.models import Profile, User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth import get_user
from django.db.models import Q


# Create your views here.
def bookRecipes(request):
    all_recipes = Recipe.objects.all()
    context={
        'all_recipes' : all_recipes
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
        dict[ingredient] = str(ingredient.quantity_set.filter(recipe=single_recipe).values_list('value', flat=True).get()) + " " + str(ingredient.unit_set.filter(recipe=single_recipe).values_list('unit', flat=True).get())

    return render(request, 'recipes/single_recipe.html', {'single_recipe': single_recipe, 'dict': dict})


def new_recipe(request):
    if request.user is not None:
        if request.user.is_authenticated:
            return render(request, 'recipes/recipe_form.html')
        return HttpResponseNotFound('<h1>Page not found</h1>')


def result_of_addition_recipe(request):
    u = get_user(request)
    if u is not None:
        if u.is_authenticated and request.POST['name'] and request.POST['i0'] and request.POST['instruction']:
            profile = Profile.objects.get(user=u)
            new_recipe = Recipe(author=profile, title=request.POST['name'], likes=0, instruction=request.POST['instruction'], level=request.POST['level'])
            new_recipe.save()
            for i in range(int(request.POST['number']) + 1):
                ingredient_index = "i" + str(i)
                unit_index = "how_many" + str(i)
                try:
                    ingredient = Ingredient.objects.get(name=request.POST[ingredient_index])
                except Ingredient.DoesNotExist:
                    ingredient = Ingredient(name=request.POST[ingredient_index])
                    ingredient.save()
                try:
                    unit = Unit.objects.get(Q(unit="grams"))
                except Unit.DoesNotExist:
                    unit = Unit(unit="grams")
                    unit.save()
                try:
                    quantity = Quantity.objects.get(Q(value=request.POST[unit_index]))
                except Quantity.DoesNotExist:
                    quantity = Quantity(value=request.POST[unit_index])
                    quantity.save()
                ingredient.recipe.add(new_recipe)
                unit.recipe.add(new_recipe)
                unit.ingredient.add(ingredient)
                quantity.recipe.add(new_recipe)
                quantity.ingredient.add(ingredient)
            return render(request, 'recipes/recipe_form.html', {'result': 'True'})
        else:
            return render(request, 'recipes/recipe_form.html', {'result': 'False'})
    else:
        return redirect('users:index')


def check_database(name_of):
    try:
        if Ingredient.objects.get(Q(name=name_of)) is not None:
            return Ingredient.objects.get(Q(name=name_of))
    except Ingredient.DoesNotExist:
        return None
