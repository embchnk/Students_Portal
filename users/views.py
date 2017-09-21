from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, LoginForm
from .models import Profile, Location
from django.contrib import messages
from recipes.models import Ingredient, Recipe
from django.db.models import Count
from sqlite3 import OperationalError

def index(request):
    #- before likes means descending sorting
    try:
        recipes = Recipe.objects.all().annotate(likes_count=Count('likes')).order_by('-likes_count')[:6]
        most_popular_recipe = recipes[0]
        most_popular_recipe_list = recipes[1:6]
    except IndexError:
        most_popular_recipe = None
        most_popular_recipe_list = None
    except OperationalError:
        most_popular_recipe = None
        most_popular_recipe_list = None
    return render(request, 'users/index.html',
                  {'user': request.user,
                   'ingredients': Ingredient.objects.all(),
                   'most_popular_recipe': most_popular_recipe,
                   'most_popular_recipe_list': most_popular_recipe_list})


class UserFormView(View):
    # blueprint
    form_class = UserForm
    # html file
    template_name = 'users/registration_form.html'

    # display blank form to the user
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('users:index')

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)  # whenever user hits submit, all of that gets stored in request.POST

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            # creates an object from form but doesnt save it to database yet
            user = form.save(commit=False)
            # now clean/normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()

            # returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                # not banned, disabled, etc.
                if user.is_active:
                    login(request, user)
                    # request.user.(username,profilephoto, etc) - now we can reffer to user whenever we want
                    return redirect('users:index')
        elif form.data['password'] != form.data['password_confirm']:
            form.add_error('password_confirm', 'Passwords do not match')
        return render(request, self.template_name, {'form': form})


def login_user_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('users:index')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
        return render(request, 'users/login_form.html', {'form': LoginForm, 'LogInMsg': "Log In Here"})


class UserLoginFormView(View):
    # blueprint
    form_class = LoginForm
    # html file
    template_name = 'users/login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'login_status': True, 'LogInMsg': "Log In Here"})

    def post(self, request):
        form = self.form_class(request.POST)
        return login_user_view(request)


def logout_user_view(request):
    logout(request)
    return redirect('users:index')


def user_info(request):
    if not request.user.is_authenticated:
        return redirect('users:index')

    leaders = Profile.objects.order_by('points').all()
    locations = Location.objects.all()
    return render(request, 'users/user_info.html', {
        'user': request.user,
        'leaders': leaders,
        'locations': locations,})


def user_info_update(request):
    if not request.user.is_authenticated:
        return redirect('users:index')

    profile = request.user.profile
    if 'new-image' in request.FILES:
        image = request.FILES['new-image']
        profile.profile_image.save('image' + str(request.user.username), image)

    email = request.POST['email-edit']
    first_name = request.POST['first-name-edit']
    last_name = request.POST['last-name-edit']
    description = request.POST['description-edit']
    location_name = request.POST['location-edit']
    location = None
    if location_name != '-------------------':
        location = Location.objects.get(city_name = location_name)

    profile.user.email = email
    profile.user.first_name = first_name
    profile.user.last_name = last_name
    profile.user.save()
    profile.description = description
    profile.location = location
    profile.save()
    return redirect('users:user-info')


def user_info_change_password(request):
    if not request.user.is_authenticated:
        return redirect('users:user-info')

    oldPassword = request.POST['old-password']
    newPassword = request.POST['new-password']
    newPasswortRepeat = request.POST['new-password-repeat']
    if request.user.check_password(oldPassword) and newPassword == newPasswortRepeat:
        request.user.set_password(newPassword)
        request.user.save()

    return redirect('users:user-info')