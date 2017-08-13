from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from .models import Recipe, User, Ingredient


def index(request):
    # all_users = UserForm.objects.all()
    # context = {'all_users': all_users}
    # return render(request, 'users/index.html', context)
    return render(request, 'users/index.html')

#my book of recipes
def bookRecipes(request):
    all_recipes = Recipe.objects.all()
    context={
        'all_recipes' : all_recipes
    }
    return render(request, 'users/bookRecipes.html', context)

#my single recipe
def single_recipe(request, recipe_id):
    #try:
    #    single_recipe = Recipe.objects.get(pk=recipe_id)
    #except Recipe.DoesNotExist:
    #    raise Http404
    single_recipe = get_object_or_404(Recipe, pk=recipe_id)
    return render(request, 'users/single_recipe.html', {'single_recipe': single_recipe})

def new_recipe(request):
    return render(request, 'users/recipe_form.html')

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
        return render(request, 'users/recipe_form.html', {'result': 'True'})
    else:
        return render(request, 'users/recipe_form.html', {'result': 'False'})


def check_database(name_of):
    return Ingredient.objects.filter(name = name_of)

class UserFormView(View):
    # blueprint
    form_class = UserForm
    # html file
    template_name = 'users/registration_form.html'

    # display blank form to the user
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)  # whenever user hits submit, all of that gets stored in request.POST

        if form.is_valid():
            # creates an object from form but doesnt save it to database yet
            user = form.save(commit=False)
            # now clean/normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                # not banned, disabled, etc.
                if user.is_active:
                    login(request, user)
                    # request.user.(username,profilephoto, etc) - now we can reffer to user whenever we want
                    return redirect('users:index')

        return render(request, self.template_name, {'form': form})