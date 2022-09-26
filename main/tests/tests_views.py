from unittest import skip
from urllib import response
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from main.models import Ingredient, Recipe, Amount, StoringType, Rating, Theme
from main.views import home, createRecipe
from main.forms import RecipeForm, IngredientForm, AddForm
from django.contrib import auth
from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from categories.models import Category


class test_home(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        userobject = User.objects.create(
            username='testuser')
        userobject.set_password('testuser@123')
        userobject.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        Theme.objects.create(theme=True, user=userobject)
        # Logged in.

        self.home_url = reverse('home')
        self.empty_url = reverse('empty')

    def test_home_GET(self):
        # Mocks a call to the url and stores the response in response to be investigated:
        response = self.client.get(self.home_url)
        # Check if the response code is 200||SUCCESS
        self.assertEquals(response.status_code, 200)
        # Assert if the template used was the inteded template: base.html
        self.assertTemplateUsed(response, 'main/home.html')

    def test_empty_GET(self):
        response = self.client.get(self.empty_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_home_has_all_recipies(self):

        response = self.client.get(self.home_url)
        user = response.wsgi_request.user

       # creating a testing client:
        self.client.logout()
        userobject = User.objects.create(
            username='testuser2')
        userobject.set_password('testuser@1234')
        userobject.save()

        # Logging in with client
        self.client.login(username='testuser2',
                          password='testuser@1234')

        response2 = self.client.get(self.home_url)
        user2 = response2.wsgi_request.user

        # Create a recipe:
        Recipe.objects.create(user=user,
                              recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)

        Recipe.objects.create(user=user2,
                              recipe_name="Ramen", description="Godt", steps="100 steps to Kona", prep=60)

        # Test that home has existing recipies in the GET.
        response = self.client.get(self.home_url)
        set = Recipe.objects.all()
        # Should be : <QuerySet [<Recipe: Sushi>, <Recipe: Ramen>]>
        self.assertEqual(list(response.context.get("recipies")), list(set))


class test_createRecipe(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        userobject = User.objects.create(
            username='testuser')
        userobject.set_password('testuser@123')
        userobject.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        Theme.objects.create(theme=True, user=userobject)
        Category.objects.create(name="dinner")

    def test_createRecipe_GET(self):
        response = self.client.get(reverse('createRecipe'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_recipe.html')

    def test_createRecipe_POST(self):
        response = self.client.post(reverse(
            'createRecipe'), data={"recipe_name": "Sushi", "description": "Digg", "steps": "100 steps to Sabrura", "prep": 20, "category": 1})
        self.assertTrue(response.status_code in (
            302, 200, 301), msg="The response code: '%s' is not one of the expected: 302, 200, 301" % (response.status_code))
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEquals(
            Recipe.objects.get(recipe_name="Sushi").recipe_name, "Sushi")

    def test_createEmptyRecipe_POST(self):

        response = self.client.post(reverse(
            'createRecipe'), data={"recipe_name": "", "description": "", "steps": "", "prep": "", "category": 1})
        self.assertTrue(response.status_code in (
            302, 200, 301), msg="The response code: '%s' is not one of the expected: 302, 200, 301" % (response.status_code))
        self.assertEqual(Recipe.objects.count(), 0)

    def test_faultyRecipe_POST(self):
        response = self.client.post(reverse(
            'createRecipe'), data={"recipe_name": "", "description": "Digg", "steps": "100 steps to Sabrura", "prep": "20", "category": 1})
        self.assertTrue(response.status_code in (
            302, 200, 301), msg="The response code: '%s' is not one of the expected: 302, 200, 301" % (response.status_code))
        self.assertEqual(Recipe.objects.count(), 0)

    def test_defaultimage_Recipe_POST(self):
        self.client.post(reverse(
            'createRecipe'), data={"recipe_name": "Sushi", "description": "Digg", "steps": "100 steps to Sabrura", "prep": 20, "category": 1})
        recipe = Recipe.objects.get(id=1)
        self.assertEquals("food.png", recipe.avatar,
                          "The default image is not set to food.png")

    def test_image_Recipe_POST(self):
        # Find image path
        imagePath = finders.find('images/sushi.jpg')
        # Ope image with path
        image = SimpleUploadedFile(
            name='TestImage.PNG',
            content=open(imagePath, 'rb').read(),
            content_type='image/PNG')
        # Structure data to POST
        data = {
            "recipe_name": "Sushi",
            "description": "Digg",
            "steps": "100 steps to Sabrura",
            "prep": 20,
            "avatar": image,
            "category": 1}
        # Post data to "createRecipe"
        response = self.client.post(reverse(
            'createRecipe'), data)

        # Get the new recipe
        recipe = Recipe.objects.get(id=1)

        self.assertNotEquals("food.png", recipe.avatar,
                             "The default image is still set to the default: food.png, even when we posten another image")

        self.assertEquals(image.size, recipe.avatar.size,
                          "The images are not exactly the same size, so it must be something wrong here")


class test_recipe_view(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        userobject = User.objects.create(
            username='testuser')
        userobject.set_password('testuser@123')
        userobject.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        Theme.objects.create(theme=True, user=userobject)
        Category.objects.create(name="dinner")

    def test_recipe_view_GET(self):
        self.client.post(reverse(
            'createRecipe'), data={"recipe_name": "Sushi", "description": "Digg", "steps": "100 steps to Sabrura", "prep": 20, "category": 1})

        recId = Recipe.objects.get(recipe_name="Sushi").id
        recipe_view_url = reverse("recipeView", args=[recId])
        GETresponse = self.client.get(recipe_view_url)
        self.assertEquals(GETresponse.status_code, 200)
        self.assertTemplateUsed(GETresponse, 'main/recipe_view.html')

    def verify_user_is_shown(self):
        self.client.post(reverse(
            'createRecipe'), data={"recipe_name": "Sushi", "description": "Digg", "steps": "100 steps to Sabrura", "prep": 20, "category": 1})
        recId = Recipe.objects.get(recipe_name="Sushi").id
        recipe_view_url = reverse("recipeView", args=[recId])
        response = self.client.get(recipe_view_url)

        self.assertContains(response, 'Created by: testuser',
                            "User is not shown correctly in recipy in format 'created by testuser'")

    def test_faulty_recipe_view_GET(self):
        recipe_view_url = reverse("recipeView", args=[999])
        GETresponse = self.client.get(recipe_view_url)
        self.assertEquals(GETresponse.status_code, 200)
        self.assertTemplateUsed(GETresponse, 'main/home.html')


class test_mypage(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        userobject = User.objects.create(
            username='testuser')
        userobject.set_password('testuser@123')
        userobject.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        Theme.objects.create(theme=True, user=userobject)
        # Logged in.

    def test_mypage_GET(self):
        # Mocks a call to the url and stores the response in response to be investigated:
        response = self.client.get(reverse("mypage"))
        # Check if the response code is 200||SUCCESS
        self.assertEquals(response.status_code, 200)
        # Assert if the template used was the inteded template: base.html
        self.assertTemplateUsed(response, 'main/mypage.html')

    def test_mypage_has_my_recipies(self):
        response = self.client.get(reverse("mypage"))
        user = response.wsgi_request.user

       # creating a testing client:
        self.client.logout()
        userobject = User.objects.create(
            username='testuser2')
        userobject.set_password('testuser@1234')
        userobject.save()

        # Logging in with client
        self.client.login(username='testuser2',
                          password='testuser@1234')

        response2 = self.client.get(reverse("mypage"))
        user2 = response2.wsgi_request.user

        # Create a recipe:
        Recipe.objects.create(user=user,
                              recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)

        Recipe.objects.create(user=user2,
                              recipe_name="Ramen", description="Godt", steps="100 steps to Kona", prep=60)

        # Test that home has existing recipies in the GET.
        response3 = self.client.get(reverse("mypage"))

        self.assertContains(response3, '"card-title">Ramen')
        self.assertNotContains(response3, '"card-title">Sushi')

    def test_mypage_delete_recipe(self):
        response = self.client.get(reverse("mypage"))
        user = response.wsgi_request.user
        recipe = Recipe.objects.create(user=user,
                                       recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)

        self.assertEquals(
            Recipe.objects.get(recipe_name="Sushi").recipe_name, "Sushi")

        self.client.post(reverse("mypage"), {"recipeID": recipe.id})

        self.assertEquals(
            list(Recipe.objects.all()), list())


class test_addIngredient(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        userobject = User.objects.create(
            username='testuser')
        userobject.set_password('testuser@123')
        userobject.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        # Logged in.
        recipe = Recipe.objects.create(
            recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)
        self.recId = recipe.id
        Theme.objects.create(theme=True, user=userobject)

    def test_add_ingredient_GET_404(self):
        response = self.client.get(
            'add_ingredients')
        self.assertEquals(response.status_code, 404)

    def test_add_ingredient_GET_200(self):
        response = self.client.get(
            reverse('add_ingredients', args=[self.recId]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_ingredients.html')

    def test_add_ingredient_GET(self):
        response = self.client.get(
            reverse('add_ingredients', args=[self.recId]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_ingredients.html')

    def test_add_ingredient_GET_REDIRECT(self):
        response = self.client.get(
            reverse("add_ingredients", args=[999]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_add_ingredient_POST(self):
        # Populating the database
        storing_type = StoringType.objects.create(storing_type='gram')
        recipe = Recipe.objects.create(
            recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)
        recId = recipe.id
        ingredient = Ingredient.objects.create(
            ingredient_name='Laks', storing_type=storing_type)
        # Done pupulating database

        response = self.client.post(reverse("add_ingredients", args=[recId]),
                                    data={'ingredient': ingredient.id, 'amount': "10", 'formtype': "add ingredient to recipe"})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/add_ingredients.html')
        amount = Amount.objects.get(recipe=recipe)
        self.assertEquals(amount.ingredient, ingredient,
                          "The ingredient is not added to the recipy in views.add_ingredients_view")

    def test_create_ingredient_POST(self):
        # Populating the database
        storing_type = StoringType.objects.create(storing_type='gram')
        recipe = Recipe.objects.create(
            recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)
        recId = recipe.id
        # Done pupulating database

        response = self.client.post(reverse("add_ingredients", args=[recId]),
                                    data={
            'ingredient_name': "Laks", 'storing_type': storing_type.id, 'formtype': "add ingredient to list"})
        self.assertTrue(response.status_code in (
            302, 200, 301), "The response code: '%s' is not one of the expected: 302, 200, 301" % (response.status_code))
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertEquals(
            Ingredient.objects.get(ingredient_name="Laks").ingredient_name, "Laks", "The POST to views.add_ingredients_view failed to create a new ingredient")

    def test_create_nameless_ingredient_GET(self):

        # Populating the database
        storing_type = StoringType.objects.create(storing_type='gram')
        recipe = Recipe.objects.create(
            recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)
        recId = recipe.id
        # Done pupulating database

        response = self.client.post(reverse("add_ingredients", args=[recId]),
                                    data={'ingredient_name': " ", 'storing_type': storing_type.id, 'formtype': "add ingredient to list"})
        self.assertTrue(response.status_code in (
            302, 200, 301), "The response code: '%s' is not one of the expected: 302, 200, 301" % (response.status_code))
        self.assertEquals(
            Ingredient.objects.count(), 0, "The POST to views.add_ingredients_view failed to create a new ingredient")


class test_edit_recipe_data(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        userobject = User.objects.create(
            username='testuser')
        userobject.set_password('testuser@123')
        userobject.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        Theme.objects.create(theme=True, user=userobject)
        # Logged in.

    def test_change_data(self):

        # Populating the database
        Category.objects.create(name="dinner")
        storing_type = StoringType.objects.create(storing_type='gram')
        recipe = Recipe.objects.create(
            recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)
        recId = recipe.id

        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEquals(
            Recipe.objects.get(recipe_name="Sushi").recipe_name, "Sushi")

        self.client.post(reverse(
            "updateRecipe", args=[recId]), data={"recipe_name": "Sushi", "description": "Digg", "steps": "100 steps to Sabrura", "prep": 30, "category": 1})

        self.assertEquals(
            Recipe.objects.get(recipe_name="Sushi").prep, 30)
        self.assertEqual(Recipe.objects.count(), 1)


class test_rate_recipe(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        userobject = User.objects.create(
            username='testuser')
        userobject.set_password('testuser@123')
        userobject.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        # Logged in.
        self.recipe = Recipe.objects.create(
            recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)
        self.recId = self.recipe.id

        self.response = self.client.post(reverse(
            "recipeView", args=[self.recId]), data={"rating": 3})

    def test_rate_post(self):

        self.assertEquals(self.response.status_code, 200,
                          "Something went wrong in posting a new rating")
        self.assertEquals(Rating.objects.count(), 1,
                          "The rating was not properly saved in database.")

    def test_update_rate(self):
        self.response = self.client.post(reverse(
            "recipeView", args=[self.recId]), data={"rating": 5})
        self.assertEquals(Rating.objects.count(), 1,
                          "The rating was most likely duplicated in the database")

        self.assertEquals(Rating.objects.get(recipe=self.recId).rating,
                          5, "The new updated value was not stored in database")


class test_popular(TestCase):
    def setUp(self):
        # creating a testing client:
        self.client = Client()
        # Logging in with client
        self.user = User.objects.create(
            username='testuser')
        self.user.set_password('testuser@123')
        self.user.save()
        self.client.login(username='testuser',
                          password='testuser@123')
        # Logged in.
        self.sushi = Recipe.objects.create(user=self.user,
                                           recipe_name="Sushi", description="Digg", steps="100 steps to Sabrura", prep=20)

        self.ramen = Recipe.objects.create(user=self.user,
                                           recipe_name="Ramen", description="Godt", steps="100 steps to Kona", prep=60)

    def test_popular(self):
        response = self.client.get(reverse('popular'))
        ordered_recipe_list = response.context.get("recipes")

        self.assertEquals(ordered_recipe_list, [
        ], "There should be shown no unrated recipes in the popular page.")

        Rating.objects.create(rating=3, recipe=self.sushi, user=self.user)
        response = self.client.get(reverse('popular'))
        ordered_recipe_list = response.context.get("recipes")
        self.assertEquals(ordered_recipe_list, [
                          self.sushi], "Rated items should show up")

        Rating.objects.create(rating=2, recipe=self.ramen, user=self.user)

        response = self.client.get(reverse('popular'))
        ordered_recipe_list = response.context.get("recipes")

        self.assertEquals(ordered_recipe_list, [
                          self.sushi, self.ramen], "All rated items should show up and ordered")
        Rating.objects.update_or_create(
            rating=5, recipe=self.ramen, user=self.user)

        response = self.client.get(reverse('popular'))
        ordered_recipe_list = response.context.get("recipes")

        self.assertEquals(ordered_recipe_list, [
            self.ramen, self.sushi], "Rated items should change order depending on rating")


"""        self.response = self.client.post(reverse(
            "recipeView", args=[self.recId]), data={"rating": 3})"""
