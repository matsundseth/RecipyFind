from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .forms import RecipeForm, IngredientForm, AddForm, RatingForm
from .models import Rating, Recipe, Amount, Shoppinglist, Theme
from categories.models import Category
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
import json

# Create your views here.


@login_required(login_url='/login/')
def updateRecipe(response, pk):
    recipe = Recipe.objects.get(id=pk)
    form = RecipeForm(instance=recipe)

    if response.method == 'POST':
        form = RecipeForm(response.POST, response.FILES, instance=recipe)
        if form.is_valid:
            form.save()
            return redirect('/add_ingredients/' + str(pk))
    user = get_user(response)
    allCategories = Category.objects.all()
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()

    return render(response, 'main/update_recipe.html', {'form': form, 'bool': theme.theme, "allCategories": allCategories})


@login_required(login_url='/login/')
def home(response):
    recipes = Recipe.objects.all()
    user = get_user(response)
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()
    ratings = Rating.objects.all()
    allCategories = Category.objects.all()
    # Just need to create a dictinary of ratings for each of the recipes:
    ratings = {}
    for recipe in recipes:
        ratingArray = []
        for rating in recipe.rating_set.all():
            ratingArray.append(rating.rating)
        ratings[recipe.id] = ratingArray

    # Now that i have a valid dictionary, let's write it into JSON so i can parse it in javascript
    ratingsJson = json.dumps(ratings)
    return render(response, "main/home.html", {"recipies": recipes, "bool": theme.theme, "ratingsJson": ratingsJson, "allCategories": allCategories})


@login_required(login_url='/login/')
def recipe_view(response, pk):
    user = get_user(response)
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()

    allCategories = Category.objects.all()
    try:
        recipe = Recipe.objects.get(pk=pk)
    except(Recipe.DoesNotExist):
        recipies = Recipe.objects.all()
        return render(response, "main/home.html", {"recipies": recipies, "allCategories": allCategories, 'bool': theme.theme})
    amounts = Amount.objects.filter(recipe=recipe)

    # Posting a rating on this recipe, for a user.
    if response.method == "POST":
        try:
            # If the user has rated recipe before: only add rating
            rating = Rating.objects.get(user=response.user, recipe=recipe)
            form = RatingForm(response.POST, instance=rating)
        except(Rating.DoesNotExist):
            # If the user has not rated recipe before: Add user and recipe and rating
            form = RatingForm(response.POST)
            form.instance.recipe = recipe
            form.instance.user = response.user

        if form.is_valid():
            form.save()

    ratingArray = []
    for rating in recipe.rating_set.all():
        ratingArray.append(rating.rating)

    return render(response, "main/recipe_view.html",
                  {"recipe": recipe, "amounts": amounts, 'bool': theme.theme, 'ratingArray': ratingArray, "allCategories": allCategories})


@login_required(login_url='/login')
def mypage(response):

    if response.method == "POST":
        Recipe.objects.filter(id=response.POST["recipeID"]).delete()

    recipies = Recipe.objects.all()
    user = get_user(response)
    allCategories = Category.objects.all()
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()

    return render(response, "main/mypage.html", {"recipies": recipies, "bool": theme.theme, "allCategories": allCategories})


def theme(response):
    if response.method == 'POST':

        user = get_user(response)

        if Theme.objects.filter(user=user).exists():
            theme = Theme.objects.filter(user=user).get()

            theme.theme = not theme.theme
            theme.save()

        else:
            theme = Theme(theme=False, user=user)
            theme.save()

    recipies = Recipe.objects.all()

    return HttpResponseRedirect("/mypage/")


@login_required(login_url='/login/')
def createRecipe(response):
    user = get_user(response)
    allCategories = Category.objects.all()
    if response.method == "POST":
        form = RecipeForm(response.POST, response.FILES)
        form2 = ContainsForm(response.POST)

        if form.is_valid() and form2.is_valid():

            response.user.recipe.add(form.save())
            form2.instance.recipe = form.instance
            form2.save()

            return HttpResponseRedirect("/add_ingredients/%s" % (form.instance.id))

    else:
        form = RecipeForm()
        form2 = ContainsForm()
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = False

    return render(response, "main/create_recipe.html", {"form": form, 'form2': form2, 'bool': theme.theme, "allCategories": allCategories})


@login_required(login_url='/login/')
def add_ingredients_view(response, pk):
    allCategories = Category.objects.all()
    try:
        rec = Recipe.objects.get(pk=pk)
    except(Recipe.DoesNotExist):
        recipies = Recipe.objects.all()
        theme = Theme.objects.filter(user=get_user(response)).get()

        return render(response, "main/home.html", {"recipies": recipies, 'bool': theme.theme, "allCategories": allCategories})

    amounts = Amount.objects.all().filter(recipe=rec)
    if response.method == "POST":
        formtype = response.POST["formtype"]
        if formtype == "add ingredient to recipe":
            form = AddForm(response.POST)
            if form.is_valid():
                form.instance.recipe = rec
                form.save()

        if formtype == "add ingredient to list":
            form = IngredientForm(response.POST)
            if form.is_valid():
                form.save()

    form = AddForm()
    form2 = IngredientForm()
    user = get_user(response)
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = False

    return render(response, "main/add_ingredients.html", {'rec': rec, 'form': form, 'form2': form2, 'amounts': amounts, 'bool': theme.theme, "allCategories": allCategories})


@login_required(login_url='/login/')
def popular(response):
    allCategories = Category.objects.all()
    recipes = Recipe.objects.all()
    user = get_user(response)
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()
    ratings = Rating.objects.all()
    # Just need to create a dictinary of ratings for each of the recipes: recID: [ratings]
    ratings = {}
    for recipe in recipes:
        ratingSum = 0
        allRatings = recipe.rating_set.all()
        for rating in allRatings:
            ratingSum += rating.rating
        if ratingSum != 0:
            ratings[recipe.id] = ratingSum / allRatings.count()

    # Then create a list of each recipy mena value: Sorted!
    sorted_values = sorted(ratings.values(), reverse=True)
    # Then use this list to sort the dictionary above!
    # This is to get a sorted dictinary of recipe ID to meanScores:
    sorted_recipy_ratings = {}
    for i in sorted_values:
        for k in ratings.keys():
            if ratings[k] == i:
                sorted_recipy_ratings[k] = ratings.pop(k)
                break

    # Now then, to present the recipes in ordered fashion, i need to send in the recipes in that order and no more than 10!.
    recipeList = []
    for recId in sorted_recipy_ratings:
        recipeList.append(Recipe.objects.get(id=recId))
        if len(recipeList) >= 10:
            break

    # Now that i have a valid, sorted dictionary of mean ratings, let's write it into JSON so i can parse it in javascript
    # and make the stars shine.
    ratingsJson = json.dumps(sorted_recipy_ratings)

    return render(response, "main/popular.html", {"recipes": recipeList, "bool": theme.theme, "ratingsJson": ratingsJson, "allCategories": allCategories})


@login_required(login_url='/login/')
def shoppinglist(response):
    allCategories = Category.objects.all()
    user = get_user(response)
    try:
        list = Shoppinglist.objects.get(user=user)
    except(Shoppinglist.DoesNotExist):
        list = Shoppinglist(user=user)
        list.save()
    if response.method == "POST":
        list.shoppinglist.remove(response.POST["amountID"])

    ingredients = list.shoppinglist.all()
    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()

    return render(response, "main/shoppinglist.html", {'bool': theme.theme, 'ingredients': ingredients, "allCategories": allCategories})


@login_required(login_url='/login/')
def add_shopping_cart(response, pk):
    allCategories = Category.objects.all()
    try:
        recipe = Recipe.objects.get(pk=pk)
    except(Recipe.DoesNotExist):
        recipies = Recipe.objects.all()
        return render(response, "main/home.html", {"recipies": recipies})
    amounts = Amount.objects.filter(recipe=recipe)
    user = get_user(response)

    try:
        theme = Theme.objects.filter(user=user).get()
    except(Theme.DoesNotExist):
        theme = Theme(theme=False, user=user)
        theme.save()

    # Posting a rating on this recipe, for a user.
    if response.method == "POST":
        try:
            list = Shoppinglist.objects.filter(user=user).get()
            for amount in amounts:
                list.shoppinglist.add(amount.id)
            list.save()
        except(Shoppinglist.DoesNotExist):
            list = Shoppinglist(user=user)
            list.save()
            for amount in amounts:
                list.shoppinglist.add(amount.id)
            list.save()
    ratingArray = []
    for rating in recipe.rating_set.all():
        ratingArray.append(rating.rating)

    return render(response, "main/recipe_view.html",
                  {"recipe": recipe, "amounts": amounts, 'bool': theme.theme, 'ratingArray': ratingArray, "allCategories": allCategories})
