from django import forms

from categories.models import Contains
from .models import Ingredient, Recipe, Amount, Rating


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = []
        widgets = {
            'ingredient_name': forms.TextInput(attrs={'class': 'ingredient_name_input'})}


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['ingredients', 'user']


class AddForm(forms.ModelForm):
    class Meta:
        model = Amount
        exclude = ['recipe']
        widgets = {
            'IngredientNameField': forms.TextInput(attrs={'class': 'IngredientNameTextField'})}


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['user', 'recipe']

class ContainsForm(forms.ModelForm):
    class Meta:
        model = Contains
        exclude = ['recipe']
