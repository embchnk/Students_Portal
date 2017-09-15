from .models import Recipe, Ingredient, Unit, Quantity
from users.models import Profile, User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from users.forms import LoginForm
import json


# Create your views here.
def bookRecipes(request):
    all_recipes = Recipe.objects.all()
    context = {
        'all_recipes': all_recipes
    }
    return render(request, 'recipes/bookRecipes.html', context)


# my single recipe
def single_recipe(request, recipe_id):

    single_recipe = get_object_or_404(Recipe, pk=recipe_id)

    referer = request.META.get('HTTP_REFERER')
    try:
        if 'recipe_matcher/recipe-matcher' in referer:
            ingredients = request.session['ingredients']
            missing = {}
            if ingredients is not None:
                request.session.modified = True
                for ingredient in single_recipe.ingredient_set.all():
                    if str(ingredient.pk) not in ingredients:
                        missing[ingredient.name] = ingredient
        else:
            missing = {}
    except TypeError:
        missing = {}
    except KeyError:
        missing = {}
    thumb_is_up = False

    try:
        u = get_user(request)
        if single_recipe.likes.filter(user=u).count():
            thumb_is_up= True
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

    return render(request, 'recipes/single_recipe.html', {'single_recipe': single_recipe, 'dict': dict,
                                                          'thumb_is_up': thumb_is_up, 'missing': missing})


def likes(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    try:
        u = get_user(request)
        if recipe.likes.filter(user=u).count():
            recipe.likes.remove(Profile.objects.get(user=u))
        else:
            recipe.likes.add(Profile.objects.get(user=u))
            recipe.save()
    except:
        #I must complete content of except
        u='something'
    return single_recipe(request, recipe_id)


def new_recipe(request):
    if request.user is not None:
        if request.user.is_authenticated:
            return render(request, 'recipes/recipe_form.html', {'unit_class': Unit.objects.all()})
        return render(request, 'users/login_form.html', {'form': LoginForm, 'LogInMsg': 'You need to log in to add recipe'})


def result_of_addition_recipe(request):
    u = get_user(request)
    if u is not None:
        if u.is_authenticated and request.POST['name'] and request.POST['i0'] and request.POST['instruction']:
            profile = Profile.objects.get(user=u)
            new_recipe = Recipe(author=profile, title=request.POST['name'],
                                instruction=request.POST['instruction'], level=request.POST['level'], dish_photo=request.POST['dish_photo'])
            new_recipe.save()
            for i in range(int(request.POST['number']) + 1):
                ingredient_index = "i" + str(i)
                unit_index = "unit" + str(i)
                quantity_index = "quantity" + str(i)
                try:
                    ingredient = Ingredient.objects.get(name=request.POST[ingredient_index].lower())
                except Ingredient.DoesNotExist:
                    ingredient = Ingredient(name=request.POST[ingredient_index].lower())
                    if not ingredient.__str__():
                        continue
                    else:
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
                except ValueError:
                    continue
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


def get_ingredients(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        ingredients = Ingredient.objects.filter(name__icontains=q)
        results = []
        for ingredient in ingredients:
            place_json = {}
            place_json = ingredient.name
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)