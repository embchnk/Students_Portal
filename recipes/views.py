from .models import Recipe, Ingredient
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
    return render(request, 'recipes/single_recipe.html', {'single_recipe': single_recipe})


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
                temp_i = 'i'+str(i)
                temp_how_many = 'how_many'+str(i)
                # now i check if ingredient is located in our database
                how_many = "none"
                if request.POST[temp_how_many] is not None:
                    how_many = request.POST[temp_how_many]
                if check_database(request.POST[temp_i], how_many) is None:
                    ingredient = Ingredient(name=request.POST[temp_i], how_many=how_many)
                    ingredient.save()
                else:
                    ingredient = check_database(request.POST[temp_how_many], how_many)
                ingredient.recipe.add(new_recipe)
            return render(request, 'recipes/recipe_form.html', {'result': 'True'})
        else:
            return render(request, 'recipes/recipe_form.html', {'result': 'False'})
    else:
        return redirect('users:index')


def check_database(name_of, how_many):
    try:
        if Ingredient.objects.get(Q(name=name_of) & Q(how_many=how_many)) is not None:
            return Ingredient.objects.get(Q(name=name_of) & Q(how_many=how_many))
    except Ingredient.DoesNotExist:
        return None
