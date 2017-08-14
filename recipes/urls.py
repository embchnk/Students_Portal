from django.conf.urls import url
from . import views

app_name = 'recipes'

urlpatterns = [
    url(r'^new_recipe/$', views.new_recipe, name='new_recipe'),
    url(r'^result/$', views.result_of_addition_recipe, name='result_of_addition_recipe'),
    url(r'^bookRecipes/$', views.bookRecipes, name='bookRecipes'),
    url(r'^bookRecipes/(?P<recipe_id>[0-9]+)$', views.single_recipe, name='single_recipe')
]
