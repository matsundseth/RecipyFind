from django.test import TestCase
from main.models import Ingredient, Recipe, Amount


class TestModels(TestCase):

    def setUp(self):
        self.rec1 = Ingredient.objects.create(
            ingredient_name='Ing1',
            storing_type='stk'
        )
