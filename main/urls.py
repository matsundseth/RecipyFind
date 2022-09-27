from django.urls import path
from django.urls import path, include

from categories.views import category_view
from . import views  # from . means from this current folder.

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="empty"),
    path("createRecipe/", views.createRecipe, name="createRecipe"),
    path("recipe_view/<int:pk>", views.recipe_view, name="recipeView"),
    path('add_ingredients/<int:pk>',
         views.add_ingredients_view, name='add_ingredients'),
    path("mypage/", views.mypage, name="mypage"),
    path("update-recipe/<int:pk>", views.updateRecipe, name="updateRecipe"),
    path('mypage/theme/', views.theme, name='theme'),
    path('popular/', views.popular, name='popular'),
    path('category/<int:pk>', category_view, name='categories'),
    path('shoppinglist/', views.shoppinglist, name='shoppinglist'),
    path('add_shopping_cart/<int:pk>',
         views.add_shopping_cart, name='add_shopping_cart'),
]
