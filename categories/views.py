from unicodedata import category
from django.shortcuts import render

from categories.models import Category, Contains
from main.models import Theme, Recipe
from django.contrib.auth import *
import json
# Create your views here.


def category_view(response, pk):
    category = Category.objects.get(pk=pk)
    recipes = Recipe.objects.all()
    contains = Contains.objects.filter(category=category)
    allCategories = Category.objects.all()
    user = get_user(response)
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()
    ratings = {}
    for recipe in recipes:
        ratingArray = []
        for rating in recipe.rating_set.all():
            ratingArray.append(rating.rating)
        ratings[recipe.id] = ratingArray

    # Now that i have a valid dictionary, let's write it into JSON so i can parse it in javascript
    ratingsJson = json.dumps(ratings)
    return render(response, 'main/categories.html', {"contains": contains, 'bool': theme.theme, "allCategories": allCategories, "name": category.name, "ratingsJson": ratingsJson})
