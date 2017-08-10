from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm


def index(request):
    # all_users = UserForm.objects.all()
    # context = {'all_users': all_users}
    # return render(request, 'users/index.html', context)
    return render(request, 'users/index.html')


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
                    redirect('users:index')

            return render(request, self.template_name, {'form': form})
