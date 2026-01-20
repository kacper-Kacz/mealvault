from django import forms
from django.core.exceptions import ValidationError
from .models import Recipe, Ingredient, MealPlan

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "description", "servings", "is_premium")

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise ValidationError("Title must be at least 3 characters long.")
        return title

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ("name", "quantity", "unit")

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = ("name", "notes", "week_start", "recipes")

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise ValidationError("Name must be at least 3 characters long.")
        return name
