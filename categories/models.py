from django.db import models
from main.models import Recipe

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contains(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name + ' ' + self.recipe.recipe_name
