from django.urls import path
from . import views

app_name = "vault"

urlpatterns = [
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/new/", views.recipe_create, name="recipe_create"),
    path("recipes/<int:pk>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipes/<int:pk>/delete/", views.recipe_delete, name="recipe_delete"),
    path("ingredients/<int:pk>/delete/", views.ingredient_delete, name="ingredient_delete"),

    path("mealplans/", views.mealplan_list, name="mealplan_list"),
    path("mealplans/new/", views.mealplan_create, name="mealplan_create"),
    path("mealplans/<int:pk>/", views.mealplan_detail, name="mealplan_detail"),
    path("mealplans/<int:pk>/edit/", views.mealplan_edit, name="mealplan_edit"),
    path("mealplans/<int:pk>/delete/", views.mealplan_delete, name="mealplan_delete"),
]
