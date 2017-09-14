from django.test import TestCase, Client
from users.models import *
from django.contrib.auth.models import User
from users.forms import UserForm


class UserFormTest(TestCase):
    def test_user_form_valid(self):
        form = UserForm(data={'username': 'temp', 'password': 'temporary', 'password_confirm': 'temporary'})
        self.assertTrue(form.is_valid())

    def test_user_form_invalid(self):
        form = UserForm(data={'username': '', 'password': 'temporary', 'password_confirm': 'temporary'})
        self.assertFalse(form.is_valid())


class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('temp', 'temp@gmail.com', 'temporary')
        self.c = Client()

    def test_add_user_valid_data(self):
        users_count = User.objects.count()
        response = self.c.post('/users/register/', {'username': 'temp2', 'password': 'temporary', 'password_confirm': 'temporary'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), users_count+1)

    def test_add_user_existing_username_create_user(self):
        users_count = User.objects.count()
        response = self.c.post('/users/register/', {'username': 'temp', 'password': 'temporary', 'password_confirm': 'temporary'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count)

    def test_add_user_not_matching_passwords_create_user(self):
        users_count = User.objects.count()
        response = self.c.post('/users/register/',
                               {'username': 'temp', 'password': 'temporary', 'password_confirm': 'temporary1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), users_count)