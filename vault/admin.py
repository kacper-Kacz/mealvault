from django.contrib import admin
from .models import Recipe, Ingredient, MealPlan

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "is_premium", "servings", "created_at")
    list_filter = ("is_premium",)
    search_fields = ("title", "description", "owner__username")
    inlines = [IngredientInline]

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "week_start", "created_at")
    search_fields = ("name", "owner__username")
