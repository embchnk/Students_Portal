from django.shortcuts import render
from .models import Recipe, Ingredient
from users.models import Profile, User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth import get_user

# Create your views here.
def bookRecipes(request):
    all_recipes = Recipe.objects.all()
    context={
        'all_recipes' : all_recipes
    }
    return render(request, 'recipes/bookRecipes.html', context)

#my single recipe
def single_recipe(request, recipe_id):
    #try:
    #    single_recipe = Recipe.objects.get(pk=recipe_id)
    #except Recipe.DoesNotExist:
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
            profile = Profile.objects.get(id=1)
            recipe = Recipe(author=profile, title=request.POST['name'], likes=0, instruction=request.POST['instruction'], level=request.POST['level'])
            recipe.save()
            for i in range(int(request.POST['number'])-1):
                iter = 'i'+str(i)
                #now i check if ingredient is located in our database
                if check_database(request.POST[iter]) is None:
                    ingredient = Ingredient(name=request.POST[iter], how_many="a little")
                    ingredient.save()
                else:
                    ingredient = check_database(request.POST[iter])
                ingredient.recipe.add(recipe)
            return render(request, 'recipes/recipe_form.html', {'result': 'True'})
        else:
            return render(request, 'recipes/recipe_form.html', {'result': 'False'})
    else:
        return redirect('users:index')

def check_database(name_of):
    if Ingredient.objects.filter(name = name_of).exists():
        return Ingredient.objects.filter(name = name_of)
    else:
        return None