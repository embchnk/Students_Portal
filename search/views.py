from django.shortcuts import render
from recipes.models import Recipe
from recipes.views import single_recipe
from django.http import HttpResponseRedirect, HttpResponse
import json


def recipe_search(request):

    q = request.GET.get('q')
    if q == "":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if q is not None:
        results = Recipe.objects.filter(title__contains=q)
        if results.count() == 1:
            return single_recipe(request, results.values_list('id', flat=True))
        return render(request, 'search/results.html', {'results': results})
    else:
        return render(request, 'search/results.html', {'results': None})


def get_recipes(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        recipes = Recipe.objects.filter(title__icontains=q)
        results = []
        for recipe in recipes:
            place_json = {}
            place_json = recipe.title
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

