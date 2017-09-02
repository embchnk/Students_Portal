from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    # example of how to translate both password fields to Polish language
    # password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    # password_confirm = forms.CharField(widget=forms.PasswordInput, label='Potwierdź hasło')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

        # example of how to translate form_fields to Polish language
        # labels = {
        #     'username': _('Nazwa użytkownika'),
        #     'email': _('Adres e-mail'),
        #     'first_name': _('Imię'),
        #     'last_name': _('Nazwisko'),
        # }


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']