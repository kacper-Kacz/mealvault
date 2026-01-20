from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recipe(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    servings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)], default=2)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=120)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit = models.CharField(max_length=30, help_text="e.g. g, ml, tbsp, pcs")

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.quantity}{self.unit})"

class MealPlan(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mealplans")
    name = models.CharField(max_length=120)
    notes = models.TextField(max_length=2000, blank=True)
    recipes = models.ManyToManyField(Recipe, blank=True, related_name="mealplans")
    week_start = models.DateField(help_text="Pick the Monday for your week.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-week_start",)

    def __str__(self):
        return self.name
