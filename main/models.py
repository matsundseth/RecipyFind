from email.policy import default
from statistics import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class StoringType(models.Model):
    storing_type = models.CharField(max_length=100)

    def __str__(self):
        return self.storing_type


class Ingredient(models.Model):

    ingredient_name = models.CharField(max_length=100)

    storing_type = models.ForeignKey(StoringType, on_delete=models.CASCADE)

    def __str__(self):
        return (self.ingredient_name + " -- " + self.storing_type.storing_type)


class Recipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipe", null=True)

    recipe_name = models.CharField(max_length=100, verbose_name="Recipe name")

    description = models.TextField(default="", verbose_name="Description")

    steps = models.TextField(default="", verbose_name="Steps")

    prep = models.IntegerField(default=0, verbose_name="Preparation time in minutes")

    # python3 -m pip install pillow
    avatar = models.ImageField(
        null=True, default="food.png", verbose_name="Add image")

    def __str__(self):
        return self.recipe_name


class Amount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    amount = models.IntegerField()

    def __str__(self):
        return ("%s: %s%s") % (self.recipe, self.ingredient, self.amount)


class Theme(models.Model):
    theme = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Rating(models.Model):
    rating = models.IntegerField(verbose_name="rating")

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return ("%s - %s: %s") % (self.user, self.recipe, self.rating)


class Shoppinglist(models.Model):
    shoppinglist = models.ManyToManyField(
        Amount, verbose_name='ShoppingList', default="")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return ("%s - Shopping list") % (self.user)
