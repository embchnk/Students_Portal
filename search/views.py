from django.shortcuts import render
from recipes.models import Recipe
from django.http import HttpResponseRedirect


def recipe_search(request):

    q = request.GET.get('q')
    if q == "":
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if q is not None:
        results = Recipe.objects.filter(title__contains=q)

        return render(request, 'search/results.html', {'results': results})
    else:
        return render(request, 'search/results.html', {'results': None})

