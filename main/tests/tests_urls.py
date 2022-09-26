from django.test import SimpleTestCase


from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import home, createRecipe, recipe_view, add_ingredients_view, mypage


class TestUrls(SimpleTestCase):
    def setUp(self):
        self.recId = 1

    def test_home_url_is_resolved(self):
        # Refering to the url name in urls.py, reverse "kind of" creates an url with this input.
        url = reverse('home')
        # prints: func=main.views.base ... etc.. This i will use to create the Equals statement.
        # print(resolve(url))
        # checking that what the url with name 'base' is "linked to" is what i expect: base.
        self.assertEquals(resolve(url).func, home)

    def test_empty_url_is_resolved(self):
        url = reverse('empty')
        self.assertEquals(resolve(url).func, home)

    def test_createRecipe_url_is_resolved(self):
        url = reverse('createRecipe')
        self.assertEquals(resolve(url).func, createRecipe)

    def test_recipe_view_is_resolved(self):
        url = reverse("recipeView", args=[self.recId])
        self.assertEquals(resolve(url).func, recipe_view)

    def test_add_ingredient_view_is_resolved(self):
        url = reverse("add_ingredients", args=[self.recId])
        self.assertEquals(resolve(url).func, add_ingredients_view)

    def test_mypage_url_is_resolved(self):
        url = reverse("mypage")
        self.assertEquals(resolve(url).func, mypage)


"""
    def test_createRecipe_url_is_resolved(self):

        #In case the view requires some input to be refered to:

        url = reverse('createRecipe', args=["ID or something"])
        self.assertEquals(resolve(url).func, createRecipe)

"""
