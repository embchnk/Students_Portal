from django.conf.urls import url
from . import views

app_name = "recipe_matcher"

urlpatterns = [
    url(r'^recipe-matcher/', views.match_recipes, name='match_recipes')
]