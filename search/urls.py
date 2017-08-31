from django.conf.urls import url
from . import views

app_name = 'search_recipe'

urlpatterns = [
    url(r'^recipes/$', views.recipe_search, name='recipe_search')
]