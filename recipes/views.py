from django.shortcuts import render
from .models import Recipe, User, Ingredient
from django.shortcuts import render, redirect, get_object_or_404

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
    return render(request, 'recipes/recipe_form.html')

def result_of_addition_recipe(request):
    if request.POST['name'] and request.POST['i0'] and request.POST['instruction']:
        r1 = Recipe(author = User.objects.first(), title=request.POST['name'], likes=0, instructions="asdfasd", level=request.POST['level'], dish_photo=request.POST['dish_photo'])
        r1.save()
        for i in range(int(request.POST['number'])-1):
            iter = 'i'+str(i)
            #now i check if ingredient is located in our database
            if check_database(request.POST[iter]) is not None:
                ingredient = check_database(request.POST[iter])
            else:
                ingredient = Ingredient(name=request.POST[iter], how_many="a little")
            ingredient.save()
            ingredient.recipe.add(r1)
        return render(request, 'recipes/recipe_form.html', {'result': 'True'})
    else:
        return render(request, 'recipes/recipe_form.html', {'result': 'False'})


def check_database(name_of):
    return Ingredient.objects.filter(name = name_of)