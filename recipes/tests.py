from django.test import TestCase
from recipes.models import *
from users.models import Profile
from django.contrib.auth.models import User


class RecipeTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username='test_user')
        test_profile = Profile.objects.create(user=test_user)
        Recipe.objects.create(author=test_profile, title='test_recipe', level='easy')

    def test_str_foo_returns_proper_value(self):
        test_recipe = Recipe.objects.get(title='test_recipe', level='easy')
        self.assertEqual(test_recipe.__str__(), 'test_recipe')


class IngredientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name='test_ingredient')

    def test_str_foo_returns_proper_value(self):
        test_ingredient = Ingredient.objects.get(name='test_ingredient')
        self.assertEqual(test_ingredient.__str__(), 'test_ingredient')