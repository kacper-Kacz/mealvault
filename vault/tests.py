from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Recipe, MealPlan

User = get_user_model()

class VaultTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="StrongPass123!")
        self.other = User.objects.create_user(username="o", password="StrongPass123!")

    def test_recipe_create_requires_login(self):
        r = self.client.get(reverse("vault:recipe_create"))
        self.assertEqual(r.status_code, 302)

    def test_owner_can_edit_recipe(self):
        self.client.login(username="u", password="StrongPass123!")
        recipe = Recipe.objects.create(owner=self.user, title="Test", description="Desc", servings=2)
        r = self.client.get(reverse("vault:recipe_edit", args=[recipe.pk]))
        self.assertEqual(r.status_code, 200)

    def test_non_owner_cannot_edit_recipe(self):
        self.client.login(username="u", password="StrongPass123!")
        recipe = Recipe.objects.create(owner=self.other, title="X", description="Y", servings=2)
        r = self.client.get(reverse("vault:recipe_edit", args=[recipe.pk]))
        self.assertEqual(r.status_code, 404)

    def test_mealplan_crud(self):
        self.client.login(username="u", password="StrongPass123!")
        recipe = Recipe.objects.create(owner=self.user, title="R", description="D", servings=2)
        r = self.client.post(reverse("vault:mealplan_create"), {
            "name": "Week plan",
            "notes": "notes",
            "week_start": date.today(),
            "recipes": [recipe.pk],
        })
        self.assertIn(r.status_code, (200, 302))
        self.assertTrue(MealPlan.objects.filter(owner=self.user, name="Week plan").exists())
