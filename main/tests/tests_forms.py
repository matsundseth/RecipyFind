from django.test import TestCase
from main.forms import IngredientForm, AddForm, RecipeForm

from unittest import skip

from main.models import Ingredient, Recipe, StoringType


class TestForms(TestCase):

    def test_IngredientForm(self):

        storing_type = StoringType.objects.create(storing_type='stk')
        form = IngredientForm(data={'ingredient_name': 'mel',
                                    'storing_type': storing_type
                                    })
        self.assertTrue(form.is_valid())

    def test_IngredientForm_empty(self):
        form = IngredientForm(data={})

        self.assertFalse(form.is_valid())
        self.assertAlmostEquals(len(form.errors), 2)

    def test_RecipeForm(self):
        form = RecipeForm(data={'recipe_name': 'kake',
                          'description': '0', 'steps': '0', 'prep': 1})

        self.assertTrue(form.is_valid())

    def test_RecipeForm_empty(self):
        form = RecipeForm(data={})

        self.assertFalse(form.is_valid())
        self.assertAlmostEquals(len(form.errors), 4)

    def test_AddForm(self):

        storing_type = StoringType.objects.create(storing_type='stk')
        ingred = Ingredient.objects.create(ingredient_name='mel',
                                           storing_type=storing_type
                                           )

        rec1 = Recipe.objects.create(
            recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)

        form = AddForm(data={'ingredient': ingred,
                             'amount': "1"})
        self.assertTrue(form.is_valid())

    def test_AddForm_empty(self):
        form = AddForm(data={})

        self.assertFalse(form.is_valid())
        self.assertAlmostEquals(len(form.errors), 2)
